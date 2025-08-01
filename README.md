# Automação OnBase POUPEX FHE

## 📋 Visão Geral

Este projeto automatiza o processo de classificação e organização de documentos no sistema OnBase da POUPEX FHE, eliminando a necessidade de classificação manual e garantindo que cada documento seja direcionado automaticamente para o setor correto.

## 🎯 Objetivos

- **Automatizar** a classificação de documentos no OnBase
- **Reduzir erros** humanos na organização de documentos
- **Acelerar** o processo de distribuição de documentos
- **Facilitar** o uso por equipes administrativas sem conhecimento técnico
- **Melhorar** a produtividade dos setores

## 🏗️ Soluções Implementadas

### 1. Solução Power Automate (Microsoft)
- **Arquivo**: `power-automate-onbase.json`
- **Descrição**: Fluxo automatizado usando Power Automate Desktop
- **Vantagens**: Interface familiar do Microsoft, fácil manutenção
- **Ideal para**: Ambientes Microsoft 365

### 2. Solução Python Avançada
- **Arquivo**: `onbase_automation.py`
- **Descrição**: Sistema completo com IA para classificação inteligente
- **Vantagens**: Mais flexível, classificação por IA, logs detalhados
- **Ideal para**: Ambiente mais técnico com maior controle

### 3. Interface Web Simples
- **Arquivo**: `web_interface.html`
- **Descrição**: Interface web para monitoramento e controle manual
- **Vantagens**: Acessível via navegador, fácil de usar
- **Ideal para**: Usuários administrativos

## 🚀 Como Começar

### Para Usuários Administrativos (Recomendado)
1. Abra o arquivo `web_interface.html` no navegador
2. Configure os setores e suas pastas correspondentes
3. Inicie o monitoramento automático
4. Acompanhe o status em tempo real

### Para Usuários Power Automate
1. Importe o arquivo `power-automate-onbase.json` no Power Automate Desktop
2. Configure as credenciais do OnBase
3. Execute o fluxo manualmente ou programe execução automática

### Para Usuários Técnicos
1. Instale Python 3.8+
2. Execute: `pip install -r requirements.txt`
3. Configure o arquivo `config.json`
4. Execute: `python onbase_automation.py`

## 📁 Estrutura do Projeto

```
projeto-onbase-automation/
├── README.md                    # Este arquivo
├── power-automate-onbase.json   # Fluxo Power Automate
├── onbase_automation.py         # Solução Python principal
├── web_interface.html           # Interface web
├── config.json                  # Configurações
├── requirements.txt             # Dependências Python
├── docs/                        # Documentação
│   ├── manual-usuario.md        # Manual para usuários
│   ├── instalacao.md           # Guia de instalação
│   └── configuracao.md         # Guia de configuração
└── logs/                       # Arquivos de log
    └── automation.log          # Log de execução
```

## ⚙️ Configuração Inicial

O sistema precisa ser configurado com:
- **Credenciais OnBase**: Usuário e senha para acesso
- **Mapeamento de Setores**: Definir quais documentos vão para quais setores
- **Regras de Classificação**: Critérios para classificação automática
- **Horários de Execução**: Quando o sistema deve executar

## 🔒 Segurança

- Credenciais criptografadas
- Logs de auditoria completos
- Backup automático de configurações
- Controle de acesso por perfil

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação em `docs/`
2. Verifique os logs em `logs/automation.log`
3. Entre em contato com a equipe de TI

## 📈 Métricas e Resultados

O sistema gera relatórios automáticos com:
- Número de documentos processados
- Taxa de acerto na classificação
- Tempo economizado
- Setores mais ativos
- Tendências de uso

---

**Desenvolvido para POUPEX FHE** - Automatização inteligente de documentos OnBase
