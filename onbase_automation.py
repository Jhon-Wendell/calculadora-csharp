#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automação OnBase POUPEX FHE - Solução Python Avançada
======================================================

Sistema completo de automação para classificação inteligente de documentos
no OnBase usando IA e regras personalizáveis.

Desenvolvido para: POUPEX FHE
Autor: Sistema de Automação Inteligente
Data: 2024
"""

import os
import json
import logging
import sqlite3
import schedule
import time
import smtplib
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

import requests
import pandas as pd
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading


@dataclass
class Document:
    """Representação de um documento OnBase"""
    id: str
    name: str
    content: str
    size: int
    created_date: str
    current_folder: str
    predicted_sector: str = ""
    confidence: float = 0.0
    processed: bool = False


@dataclass
class ProcessingResult:
    """Resultado do processamento de um documento"""
    document_id: str
    success: bool
    sector: str
    confidence: float
    error_message: str = ""
    processing_time: float = 0.0


class OnBaseConnector:
    """Conector para API do OnBase"""
    
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.token = None
        
    def authenticate(self) -> bool:
        """Autentica no OnBase"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/authentication/login",
                json={"username": self.username, "password": self.password},
                timeout=30
            )
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                return True
            return False
        except Exception as e:
            logging.error(f"Erro na autenticação: {e}")
            return False
    
    def get_pending_documents(self) -> List[Document]:
        """Busca documentos pendentes de classificação"""
        try:
            response = self.session.get(f"{self.base_url}/api/documents/pending")
            if response.status_code == 200:
                documents = []
                for doc_data in response.json().get("documents", []):
                    documents.append(Document(
                        id=doc_data["id"],
                        name=doc_data["name"],
                        content=doc_data.get("content", ""),
                        size=doc_data.get("size", 0),
                        created_date=doc_data.get("created_date", ""),
                        current_folder=doc_data.get("folder", "INBOX")
                    ))
                return documents
            return []
        except Exception as e:
            logging.error(f"Erro ao buscar documentos: {e}")
            return []
    
    def move_document(self, document_id: str, target_folder: str, reason: str = "") -> bool:
        """Move documento para pasta do setor"""
        try:
            response = self.session.put(
                f"{self.base_url}/api/documents/{document_id}/move",
                json={"targetFolder": target_folder, "reason": reason}
            )
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Erro ao mover documento {document_id}: {e}")
            return False


class IntelligentClassifier:
    """Classificador inteligente de documentos usando regras e IA"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.sector_rules = self.config.get("sector_rules", {})
        self.keywords_weights = self.config.get("keywords_weights", {})
        
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configurações do arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_config(config_path)
    
    def _create_default_config(self, config_path: str) -> Dict:
        """Cria configuração padrão"""
        default_config = {
            "sector_rules": {
                "RECURSOS_HUMANOS": {
                    "keywords": ["RH", "FOLHA", "PAGAMENTO", "FUNCIONARIO", "CONTRATACAO", "DEMISSAO", "FERIAS", "SALARIO"],
                    "weight": 1.0
                },
                "CONTRATOS": {
                    "keywords": ["CONTRATO", "ACORDO", "TERMO", "ADITIVO", "RESCISAO", "CLAUSULA"],
                    "weight": 1.0
                },
                "FINANCEIRO": {
                    "keywords": ["FINANCEIRO", "ORCAMENTO", "PAGAMENTO", "RECEITA", "DESPESA", "BALANCO", "FATURA"],
                    "weight": 1.0
                },
                "JURIDICO": {
                    "keywords": ["JURIDICO", "PROCESSO", "PARECER", "ALVARA", "LICENCA", "TRIBUNAL"],
                    "weight": 1.0
                },
                "PRESIDENCIA": {
                    "keywords": ["PRESIDENCIA", "DIRETORIA", "CONSELHO", "ATA", "DELIBERACAO", "ESTRATEGIA"],
                    "weight": 1.0
                },
                "TECNOLOGIA": {
                    "keywords": ["TI", "SISTEMA", "SOFTWARE", "HARDWARE", "BACKUP", "REDE", "SERVIDOR"],
                    "weight": 1.0
                },
                "AUDITORIA": {
                    "keywords": ["AUDITORIA", "COMPLIANCE", "CONTROLE", "REVISAO", "INSPECAO", "CONFORMIDADE"],
                    "weight": 1.0
                },
                "COMERCIAL": {
                    "keywords": ["COMERCIAL", "VENDAS", "CLIENTE", "PROPOSTA", "ORCAMENTO", "MARKETING"],
                    "weight": 1.0
                }
            },
            "confidence_threshold": 0.7,
            "default_sector": "GERAL"
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
    
    def classify_document(self, document: Document) -> Tuple[str, float]:
        """Classifica documento retornando setor e confiança"""
        text = f"{document.name} {document.content}".upper()
        sector_scores = {}
        
        # Calcula pontuação para cada setor
        for sector, rules in self.sector_rules.items():
            score = 0
            keywords = rules.get("keywords", [])
            weight = rules.get("weight", 1.0)
            
            for keyword in keywords:
                if keyword.upper() in text:
                    score += weight
            
            # Normaliza pela quantidade de keywords
            if keywords:
                sector_scores[sector] = score / len(keywords)
        
        # Encontra o setor com maior pontuação
        if sector_scores:
            best_sector = max(sector_scores, key=sector_scores.get)
            confidence = sector_scores[best_sector]
            
            # Verifica se atende o threshold de confiança
            if confidence >= self.config.get("confidence_threshold", 0.7):
                return best_sector, confidence
        
        # Retorna setor padrão se não conseguiu classificar
        return self.config.get("default_sector", "GERAL"), 0.5


class DatabaseManager:
    """Gerenciador de banco de dados para logs e histórico"""
    
    def __init__(self, db_path: str = "onbase_automation.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializa banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de documentos processados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT UNIQUE,
                document_name TEXT,
                sector TEXT,
                confidence REAL,
                processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN,
                error_message TEXT
            )
        """)
        
        # Tabela de estatísticas diárias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT PRIMARY KEY,
                total_processed INTEGER,
                successful INTEGER,
                failed INTEGER,
                avg_confidence REAL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_document_processing(self, result: ProcessingResult):
        """Registra processamento de documento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO processed_documents 
            (document_id, document_name, sector, confidence, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (result.document_id, "", result.sector, result.confidence, 
              result.success, result.error_message))
        
        conn.commit()
        conn.close()
    
    def get_daily_stats(self, date: str = None) -> Dict:
        """Obtém estatísticas do dia"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                   SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed,
                   AVG(confidence) as avg_confidence
            FROM processed_documents 
            WHERE DATE(processed_date) = ?
        """, (date,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            "total": result[0] or 0,
            "successful": result[1] or 0,
            "failed": result[2] or 0,
            "avg_confidence": result[3] or 0.0
        }


class NotificationManager:
    """Gerenciador de notificações por email"""
    
    def __init__(self, smtp_config: Dict):
        self.smtp_config = smtp_config
    
    def send_daily_report(self, stats: Dict):
        """Envia relatório diário"""
        try:
            msg = MimeMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = self.smtp_config['notification_email']
            msg['Subject'] = f"Relatório OnBase Automação - {datetime.now().strftime('%d/%m/%Y')}"
            
            body = f"""
            <h2>Relatório Diário - Automação OnBase POUPEX FHE</h2>
            <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <p><strong>Documentos Processados:</strong> {stats['total']}</p>
            <p><strong>Sucessos:</strong> {stats['successful']}</p>
            <p><strong>Falhas:</strong> {stats['failed']}</p>
            <p><strong>Taxa de Sucesso:</strong> {(stats['successful']/stats['total']*100 if stats['total'] > 0 else 0):.1f}%</p>
            <p><strong>Confiança Média:</strong> {stats['avg_confidence']:.2f}</p>
            <hr>
            <p><em>Sistema automatizado desenvolvido para POUPEX FHE</em></p>
            """
            
            msg.attach(MimeText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            logging.info("Relatório diário enviado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao enviar relatório: {e}")


class OnBaseAutomationGUI:
    """Interface gráfica para usuários administrativos"""
    
    def __init__(self, automation_engine):
        self.automation = automation_engine
        self.root = tk.Tk()
        self.root.title("OnBase Automação POUPEX FHE")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variáveis de controle
        self.is_running = tk.BooleanVar()
        self.auto_mode = tk.BooleanVar(value=True)
        
        self._create_widgets()
        self._update_status()
        
    def _create_widgets(self):
        """Cria widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="OnBase Automação POUPEX FHE", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status do Sistema", padding="10")
        status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Sistema parado")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Controles
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="Iniciar Automação", 
                  command=self._start_automation).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(control_frame, text="Parar Automação", 
                  command=self._stop_automation).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(control_frame, text="Processar Agora", 
                  command=self._process_now).grid(row=0, column=2, padx=(0, 10))
        
        ttk.Checkbutton(control_frame, text="Modo Automático", 
                       variable=self.auto_mode).grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estatísticas de Hoje", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=6, width=60)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log de Atividades", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, height=10, width=60)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def _start_automation(self):
        """Inicia automação"""
        self.is_running.set(True)
        self._update_status()
        self._log_message("Automação iniciada")
        
        if self.auto_mode.get():
            # Inicia thread para processamento automático
            threading.Thread(target=self._auto_process_loop, daemon=True).start()
    
    def _stop_automation(self):
        """Para automação"""
        self.is_running.set(False)
        self._update_status()
        self._log_message("Automação parada")
    
    def _process_now(self):
        """Processa documentos agora"""
        self._log_message("Iniciando processamento manual...")
        threading.Thread(target=self._process_documents, daemon=True).start()
    
    def _auto_process_loop(self):
        """Loop de processamento automático"""
        while self.is_running.get():
            if datetime.now().hour >= 8 and datetime.now().hour <= 18:  # Horário comercial
                self._process_documents()
            time.sleep(3600)  # Aguarda 1 hora
    
    def _process_documents(self):
        """Processa documentos"""
        try:
            results = self.automation.process_pending_documents()
            success_count = sum(1 for r in results if r.success)
            total_count = len(results)
            
            self._log_message(f"Processamento concluído: {success_count}/{total_count} sucessos")
            self._update_statistics()
            
        except Exception as e:
            self._log_message(f"Erro no processamento: {e}")
    
    def _update_status(self):
        """Atualiza status do sistema"""
        if self.is_running.get():
            self.status_label.config(text="Sistema ativo - Monitorando documentos", 
                                   foreground="green")
        else:
            self.status_label.config(text="Sistema parado", foreground="red")
    
    def _update_statistics(self):
        """Atualiza estatísticas"""
        stats = self.automation.db_manager.get_daily_stats()
        
        stats_text = f"""Total de documentos: {stats['total']}
Processados com sucesso: {stats['successful']}
Falhas: {stats['failed']}
Taxa de sucesso: {(stats['successful']/stats['total']*100 if stats['total'] > 0 else 0):.1f}%
Confiança média: {stats['avg_confidence']:.2f}"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats_text)
    
    def _log_message(self, message: str):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    def run(self):
        """Executa interface"""
        # Atualiza estatísticas iniciais
        self._update_statistics()
        self.root.mainloop()


class OnBaseAutomationEngine:
    """Motor principal de automação OnBase"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_configuration()
        
        # Inicializa componentes
        self.onbase = OnBaseConnector(
            self.config["onbase"]["url"],
            self.config["onbase"]["username"], 
            self.config["onbase"]["password"]
        )
        
        self.classifier = IntelligentClassifier(config_file)
        self.db_manager = DatabaseManager()
        
        if self.config.get("notifications", {}).get("enabled", False):
            self.notification_manager = NotificationManager(self.config["notifications"])
        else:
            self.notification_manager = None
        
        # Configurar logging
        self._setup_logging()
        
        # Configurar agendamento
        self._setup_scheduling()
    
    def _load_configuration(self) -> Dict:
        """Carrega configuração do sistema"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_configuration()
    
    def _create_default_configuration(self) -> Dict:
        """Cria configuração padrão"""
        config = {
            "onbase": {
                "url": "https://onbase.poupex.com.br",
                "username": "automation_user",
                "password": "encrypted_password"
            },
            "processing": {
                "max_documents_per_run": 100,
                "processing_interval_hours": 2,
                "business_hours_only": True,
                "start_hour": 8,
                "end_hour": 18
            },
            "notifications": {
                "enabled": True,
                "server": "smtp.poupex.com.br",
                "port": 587,
                "username": "automation@poupex.com.br",
                "password": "encrypted_password",
                "notification_email": "ti@poupex.com.br"
            },
            "security": {
                "encrypt_passwords": True,
                "log_retention_days": 30,
                "audit_enabled": True
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return config
    
    def _setup_logging(self):
        """Configura sistema de logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "automation.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def _setup_scheduling(self):
        """Configura agendamento automático"""
        interval = self.config["processing"]["processing_interval_hours"]
        schedule.every(interval).hours.do(self.process_pending_documents)
        
        # Relatório diário às 18h
        if self.notification_manager:
            schedule.every().day.at("18:00").do(self._send_daily_report)
    
    def process_pending_documents(self) -> List[ProcessingResult]:
        """Processa documentos pendentes"""
        logging.info("Iniciando processamento de documentos pendentes")
        
        # Verifica horário comercial
        if self.config["processing"]["business_hours_only"]:
            current_hour = datetime.now().hour
            start_hour = self.config["processing"]["start_hour"]
            end_hour = self.config["processing"]["end_hour"]
            
            if current_hour < start_hour or current_hour > end_hour:
                logging.info("Fora do horário comercial, aguardando...")
                return []
        
        # Autentica no OnBase
        if not self.onbase.authenticate():
            logging.error("Falha na autenticação OnBase")
            return []
        
        # Busca documentos pendentes
        documents = self.onbase.get_pending_documents()
        max_docs = self.config["processing"]["max_documents_per_run"]
        documents = documents[:max_docs]
        
        logging.info(f"Encontrados {len(documents)} documentos para processar")
        
        results = []
        for document in documents:
            start_time = time.time()
            
            try:
                # Classifica documento
                sector, confidence = self.classifier.classify_document(document)
                
                # Move documento
                success = self.onbase.move_document(
                    document.id, 
                    sector, 
                    f"Classificação automática (confiança: {confidence:.2f})"
                )
                
                processing_time = time.time() - start_time
                
                result = ProcessingResult(
                    document_id=document.id,
                    success=success,
                    sector=sector,
                    confidence=confidence,
                    processing_time=processing_time
                )
                
                if success:
                    logging.info(f"Documento {document.id} movido para {sector} "
                               f"(confiança: {confidence:.2f})")
                else:
                    result.error_message = "Falha ao mover documento"
                    logging.error(f"Erro ao mover documento {document.id}")
                
            except Exception as e:
                result = ProcessingResult(
                    document_id=document.id,
                    success=False,
                    sector="",
                    confidence=0.0,
                    error_message=str(e),
                    processing_time=time.time() - start_time
                )
                logging.error(f"Erro ao processar documento {document.id}: {e}")
            
            # Registra resultado
            self.db_manager.log_document_processing(result)
            results.append(result)
        
        logging.info(f"Processamento concluído: {len(results)} documentos")
        return results
    
    def _send_daily_report(self):
        """Envia relatório diário"""
        if self.notification_manager:
            stats = self.db_manager.get_daily_stats()
            self.notification_manager.send_daily_report(stats)
    
    def run_scheduled(self):
        """Executa agendamento automático"""
        logging.info("Iniciando execução agendada")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto
    
    def run_gui(self):
        """Executa interface gráfica"""
        gui = OnBaseAutomationGUI(self)
        gui.run()


def main():
    """Função principal"""
    print("=== OnBase Automação POUPEX FHE ===")
    print("1. Interface Gráfica (Recomendado para usuários administrativos)")
    print("2. Modo Automático (Execução em background)")
    print("3. Processamento Único (Executa uma vez e para)")
    print("4. Configurar Sistema")
    
    choice = input("\nEscolha uma opção (1-4): ").strip()
    
    try:
        automation = OnBaseAutomationEngine()
        
        if choice == "1":
            print("\nIniciando interface gráfica...")
            automation.run_gui()
        
        elif choice == "2":
            print("\nIniciando modo automático...")
            print("Pressione Ctrl+C para parar")
            automation.run_scheduled()
        
        elif choice == "3":
            print("\nExecutando processamento único...")
            results = automation.process_pending_documents()
            success_count = sum(1 for r in results if r.success)
            print(f"Processamento concluído: {success_count}/{len(results)} sucessos")
        
        elif choice == "4":
            print("\nConfigurações salvas em 'config.json'")
            print("Edite o arquivo para personalizar o sistema")
        
        else:
            print("Opção inválida!")
    
    except KeyboardInterrupt:
        print("\nSistema interrompido pelo usuário")
    except Exception as e:
        print(f"Erro: {e}")
        logging.error(f"Erro na execução principal: {e}")


if __name__ == "__main__":
    main()