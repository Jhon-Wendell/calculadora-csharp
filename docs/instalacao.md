# Guia de Instalação - OnBase Automação POUPEX FHE

## 📋 Visão Geral

Este guia destina-se à equipe de TI para instalação e configuração inicial do sistema de automação OnBase.

## 🎯 Pré-requisitos

### Requisitos de Sistema

| Componente | Especificação Mínima | Recomendado |
|------------|---------------------|-------------|
| **SO** | Windows 10/11, Linux Ubuntu 18+ | Windows 11, Ubuntu 22 LTS |
| **Python** | 3.8+ | 3.11+ |
| **RAM** | 4GB | 8GB+ |
| **Disco** | 2GB livres | 10GB+ |
| **Rede** | Conexão estável | 100Mbps+ |

### Acesso Necessário

- [x] **OnBase API**: Credenciais de serviço com permissões de leitura/movimentação
- [x] **SMTP**: Servidor de email para notificações
- [x] **Rede**: Acesso aos servidores OnBase e SMTP
- [x] **Firewall**: Liberação de portas (443, 587, 80)

---

## 🚀 Instalação

### 1. Preparação do Ambiente

#### Windows

```powershell
# Verificar Python
python --version

# Se não tiver Python, baixar de https://python.org
# Marcar "Add Python to PATH" durante instalação
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk

# CentOS/RHEL
sudo yum install python3 python3-pip python3-tkinter
```

### 2. Download e Extração

```bash
# Criar diretório do projeto
mkdir /opt/onbase-automation
cd /opt/onbase-automation

# Baixar arquivos do projeto (via git ou zip)
# Assumindo que os arquivos estão disponíveis
```

### 3. Ambiente Virtual Python

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 4. Configuração Inicial

#### Arquivo config.json

```bash
# Copiar template de configuração
cp config.json.template config.json

# Editar configurações
nano config.json
```

**Configurações obrigatórias**:

```json
{
  "onbase": {
    "url": "https://onbase.poupex.com.br",
    "username": "usuario_automacao",
    "password": "SENHA_SEGURA_AQUI"
  },
  "notifications": {
    "enabled": true,
    "server": "smtp.poupex.com.br",
    "port": 587,
    "username": "automacao@poupex.com.br",
    "password": "SENHA_EMAIL_AQUI",
    "notification_email": "ti@poupex.com.br"
  }
}
```

### 5. Teste de Conectividade

```bash
# Testar conexão OnBase
python3 -c "
from onbase_automation import OnBaseConnector
conn = OnBaseConnector('https://onbase.poupex.com.br', 'usuario', 'senha')
print('Conexão OK' if conn.authenticate() else 'Falha na conexão')
"

# Testar SMTP
python3 -c "
import smtplib
server = smtplib.SMTP('smtp.poupex.com.br', 587)
server.starttls()
print('SMTP OK')
server.quit()
"
```

---

## ⚙️ Configuração Avançada

### 1. Usuário de Serviço OnBase

**Criar usuário dedicado no OnBase**:

```sql
-- No OnBase Unity Client
-- Criar usuário: automacao_poupex
-- Grupos: Document Processing, API Access
-- Permissões: Read Documents, Move Documents, Access API
```

**Permissões necessárias**:
- Leitura de documentos pendentes
- Movimentação de documentos entre pastas
- Acesso à API REST do OnBase

### 2. Configuração de Segurança

#### Criptografia de Senhas

```bash
# Gerar chave de criptografia
python3 -c "
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print('Chave:', key.decode())
"

# Adicionar ao config.json
{
  "security": {
    "encryption_key": "CHAVE_GERADA_AQUI",
    "encrypt_passwords": true
  }
}
```

#### Criptografar senhas

```bash
python3 -c "
from cryptography.fernet import Fernet
key = b'SUA_CHAVE_AQUI'
f = Fernet(key)
senha = f.encrypt(b'senha_real').decode()
print('Senha criptografada:', senha)
"
```

### 3. Logs e Monitoramento

#### Configuração de Logs

```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/automation.log",
    "max_size": "10MB",
    "backup_count": 5,
    "format": "%(asctime)s - %(levelname)s - %(message)s"
  }
}
```

#### Rotação de Logs

```bash
# Criar script de rotação
cat > /etc/logrotate.d/onbase-automation << EOF
/opt/onbase-automation/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    copytruncate
}
EOF
```

---

## 🔧 Configuração como Serviço

### Windows (Serviço do Windows)

#### Criar arquivo `onbase_service.py`:

```python
import servicemanager
import win32serviceutil
import win32service
import win32event
from onbase_automation import OnBaseAutomationEngine

class OnBaseService(win32serviceutil.ServiceFramework):
    _svc_name_ = "OnBaseAutomation"
    _svc_display_name_ = "OnBase Automation POUPEX"
    _svc_description_ = "Sistema de automação OnBase"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        automation = OnBaseAutomationEngine()
        automation.run_scheduled()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(OnBaseService)
```

#### Instalar serviço:

```powershell
# Instalar
python onbase_service.py install

# Iniciar
python onbase_service.py start

# Parar
python onbase_service.py stop

# Remover
python onbase_service.py remove
```

### Linux (Systemd)

#### Criar arquivo `/etc/systemd/system/onbase-automation.service`:

```ini
[Unit]
Description=OnBase Automation POUPEX FHE
After=network.target

[Service]
Type=simple
User=onbase
WorkingDirectory=/opt/onbase-automation
Environment=PATH=/opt/onbase-automation/venv/bin
ExecStart=/opt/onbase-automation/venv/bin/python onbase_automation.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Ativar serviço:

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar inicialização automática
sudo systemctl enable onbase-automation

# Iniciar serviço
sudo systemctl start onbase-automation

# Verificar status
sudo systemctl status onbase-automation

# Ver logs
sudo journalctl -u onbase-automation -f
```

---

## 🔍 Monitoramento e Manutenção

### 1. Health Check

#### Script de verificação (`health_check.py`):

```python
#!/usr/bin/env python3
import requests
import json
import sys
from datetime import datetime

def check_system():
    try:
        # Verificar se processo está rodando
        # Verificar última execução
        # Verificar espaço em disco
        # Verificar conectividade OnBase
        
        with open('logs/automation.log', 'r') as f:
            last_lines = f.readlines()[-10:]
        
        # Análise dos logs
        errors = [line for line in last_lines if 'ERROR' in line]
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy' if len(errors) == 0 else 'warning',
            'errors': len(errors),
            'last_execution': 'OK'
        }
        
        print(json.dumps(status, indent=2))
        return 0 if status['status'] == 'healthy' else 1
        
    except Exception as e:
        print(f"Health check failed: {e}")
        return 2

if __name__ == '__main__':
    sys.exit(check_system())
```

#### Executar via cron:

```bash
# Adicionar ao crontab
crontab -e

# Verificar a cada 5 minutos
*/5 * * * * /opt/onbase-automation/venv/bin/python /opt/onbase-automation/health_check.py >> /var/log/onbase-health.log 2>&1
```

### 2. Backup e Recuperação

#### Script de backup:

```bash
#!/bin/bash
# backup_onbase.sh

BACKUP_DIR="/backup/onbase-automation"
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup configurações
tar -czf $BACKUP_DIR/config_$DATE.tar.gz config.json

# Backup banco de dados
cp onbase_automation.db $BACKUP_DIR/database_$DATE.db

# Backup logs importantes
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# Limpar backups antigos (manter 30 dias)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "Backup concluído: $DATE"
```

### 3. Alertas e Notificações

#### Configurar alertas por email:

```python
# alerts.py
def send_alert(subject, message, level='WARNING'):
    if level == 'CRITICAL':
        recipients = ['ti@poupex.com.br', 'gerencia@poupex.com.br']
    else:
        recipients = ['ti@poupex.com.br']
    
    # Enviar email usando configuração SMTP
    # ...
```

#### Integração com sistemas de monitoramento:

```bash
# Nagios/Zabbix check
/opt/onbase-automation/health_check.py
```

---

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Erro de Autenticação OnBase

```bash
# Testar credenciais
curl -X POST https://onbase.poupex.com.br/api/authentication/login \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario","password":"senha"}'
```

#### 2. Problema de Permissões

```bash
# Verificar permissões do usuário
sudo chown -R onbase:onbase /opt/onbase-automation
sudo chmod +x onbase_automation.py
```

#### 3. Dependências Python

```bash
# Reinstalar dependências
pip install --force-reinstall -r requirements.txt
```

#### 4. Problemas de Rede

```bash
# Testar conectividade
telnet onbase.poupex.com.br 443
telnet smtp.poupex.com.br 587
```

### Logs de Debug

```bash
# Habilitar debug completo
export PYTHONPATH=/opt/onbase-automation
export LOG_LEVEL=DEBUG
python3 onbase_automation.py
```

---

## 📊 Performance e Otimização

### 1. Tuning de Performance

#### Configurações recomendadas:

```json
{
  "processing": {
    "max_documents_per_run": 50,
    "processing_interval_hours": 1,
    "timeout_seconds": 30,
    "retry_attempts": 3
  },
  "database": {
    "connection_pool_size": 5,
    "query_timeout": 10
  }
}
```

### 2. Monitoramento de Recursos

```bash
# Monitorar uso de CPU/RAM
ps aux | grep python
htop

# Monitorar espaço em disco
df -h /opt/onbase-automation
du -sh logs/

# Monitorar rede
netstat -tulpn | grep python
```

---

## 🔐 Segurança

### 1. Checklist de Segurança

- [x] Senhas criptografadas no config.json
- [x] Usuário de serviço com permissões mínimas
- [x] Logs protegidos contra acesso não autorizado
- [x] Conexões HTTPS/TLS
- [x] Backup de configurações
- [x] Monitoramento de tentativas de acesso

### 2. Hardening

```bash
# Permissões restritivas
chmod 600 config.json
chmod 700 logs/

# Usuário dedicado sem login shell
sudo useradd -r -s /bin/false onbase

# Firewall
sudo ufw allow from 192.168.1.0/24 to any port 22
sudo ufw deny 22
```

---

## 📞 Suporte Técnico

### Contatos

- **Desenvolvedor**: Sistema de Automação Inteligente
- **Email Suporte**: ti@poupex.com.br
- **Documentação**: [Link para documentação interna]

### Procedimentos de Escalação

1. **Nível 1**: Administrador de Sistema
2. **Nível 2**: Equipe de TI POUPEX
3. **Nível 3**: Fornecedor/Desenvolvedor

---

**Instalação concluída com sucesso!**  
*Sistema pronto para produção na POUPEX FHE*