# Manual do Usuário - OnBase Automação POUPEX FHE

## 📋 Sumário

1. [Introdução](#introdução)
2. [Primeiros Passos](#primeiros-passos)
3. [Interface Web](#interface-web)
4. [Configuração](#configuração)
5. [Operação Diária](#operação-diária)
6. [Solução de Problemas](#solução-de-problemas)
7. [Suporte](#suporte)

---

## 🎯 Introdução

O **OnBase Automação POUPEX FHE** é um sistema inteligente que automatiza a classificação de documentos no OnBase, direcionando automaticamente cada documento para o setor correto da empresa.

### Benefícios
- ✅ **Economia de tempo**: Classificação automática em segundos
- ✅ **Redução de erros**: IA inteligente com 90%+ de precisão
- ✅ **Facilidade de uso**: Interface simples para qualquer usuário
- ✅ **Relatórios automáticos**: Acompanhe a produtividade em tempo real

### Setores Suportados
- 🏢 **Recursos Humanos**: Documentos de RH, folha de pagamento, contratações
- 📄 **Contratos**: Contratos, acordos, termos aditivos
- 💰 **Financeiro**: Faturas, orçamentos, pagamentos, receitas
- ⚖️ **Jurídico**: Processos, pareceres, licenças
- 🏛️ **Presidência**: Atas, deliberações, decisões estratégicas
- 💻 **Tecnologia**: Sistemas, hardware, software, redes
- 🔍 **Auditoria**: Controles, revisões, conformidade
- 🤝 **Comercial**: Vendas, clientes, propostas, marketing

---

## 🚀 Primeiros Passos

### 1. Acesso ao Sistema

**Opção A: Interface Web (Recomendada)**
1. Abra seu navegador (Chrome, Firefox, Edge)
2. Navegue até o arquivo `web_interface.html`
3. Ou abra diretamente o arquivo no navegador

**Opção B: Aplicativo Desktop**
1. Execute o arquivo `onbase_automation.py`
2. Escolha a opção "1" para interface gráfica

### 2. Primeira Configuração

Na primeira execução, você precisa:

1. **Configurar credenciais OnBase**:
   - Usuário: Seu login do OnBase
   - Senha: Sua senha do OnBase

2. **Definir horários**:
   - Horário de início: 08:00 (padrão)
   - Horário de fim: 18:00 (padrão)
   - Intervalo: A cada 2 horas (padrão)

3. **Configurar email** (opcional):
   - Email para relatórios: seu-email@poupex.com.br

---

## 🖥️ Interface Web

### Dashboard Principal

![Dashboard](./images/dashboard.png)

#### 1. **Status do Sistema**
- 🟢 **Verde**: Sistema ativo e funcionando
- 🔴 **Vermelho**: Sistema parado
- Botões de controle: Iniciar, Parar, Processar Agora

#### 2. **Estatísticas de Hoje**
- **Total**: Documentos processados hoje
- **Sucessos**: Documentos classificados corretamente
- **Falhas**: Documentos que falharam
- **Taxa de Sucesso**: Percentual de acerto (meta: >90%)

#### 3. **Setores Ativos**
Mostra quantos documentos foram enviados para cada setor

#### 4. **Log de Atividades**
Histórico em tempo real das ações do sistema

### Controles Principais

#### ▶️ **Iniciar Automação**
- Inicia o monitoramento automático
- Sistema verificará documentos no intervalo configurado
- Modo automático recomendado para operação normal

#### ⏹️ **Parar Automação**
- Para o sistema completamente
- Use apenas quando necessário parar por manutenção

#### 🔄 **Processar Agora**
- Força processamento imediato
- Útil para processar documentos urgentes
- Sistema deve estar iniciado primeiro

#### ⚙️ **Modo Automático**
- ✅ **Marcado**: Sistema funciona sozinho
- ❌ **Desmarcado**: Apenas processamento manual

---

## ⚙️ Configuração

### Configurações Básicas

#### **Intervalo de Processamento**
- **1 hora**: Para volume alto de documentos
- **2 horas**: Padrão recomendado
- **4 horas**: Para volume baixo
- **6 horas**: Verificação mínima

#### **Máximo de Documentos**
- **Padrão**: 100 documentos por execução
- **Ajuste**: Aumente se processar mais documentos

#### **Limite de Confiança**
- **Padrão**: 70% (recomendado)
- **Maior**: Menos documentos automáticos, mais precisão
- **Menor**: Mais documentos automáticos, menos precisão

### Configurações Avançadas

Para usuários técnicos, edite o arquivo `config.json`:

```json
{
  "processing": {
    "business_hours_only": true,
    "start_hour": 8,
    "end_hour": 18
  }
}
```

---

## 📅 Operação Diária

### Rotina Matinal (8:00 AM)

1. **Verificar Status**
   - Abra a interface web
   - Confirme que o sistema está ativo (🟢)
   - Verifique estatísticas do dia anterior

2. **Iniciar Automação** (se necessário)
   - Clique em "Iniciar"
   - Confirme "Modo Automático" marcado
   - Observe log de atividades

3. **Verificar Configurações**
   - Intervalo adequado para o volume esperado
   - Limite de confiança apropriado

### Durante o Dia

- **Monitoramento**: Verifique a interface ocasionalmente
- **Processamento Manual**: Use "Processar Agora" se urgente
- **Estatísticas**: Acompanhe taxa de sucesso

### Rotina Noturna (18:00 PM)

1. **Relatório Diário**
   - Revise estatísticas finais
   - Confira distribuição por setores
   - Verifique log para erros

2. **Sistema Noturno**
   - Sistema para automaticamente após 18h
   - Reinicia automaticamente às 8h (próximo dia)

### Relatórios Automáticos

O sistema envia relatórios diários por email com:
- Número total de documentos processados
- Taxa de sucesso
- Distribuição por setores
- Principais erros (se houver)

---

## 🔧 Solução de Problemas

### Problemas Comuns

#### ❌ **Sistema não inicia**
**Sintomas**: Botão "Iniciar" não funciona
**Soluções**:
1. Verifique conexão com internet
2. Confirme credenciais OnBase no `config.json`
3. Teste acesso manual ao OnBase

#### ⚠️ **Taxa de sucesso baixa (<80%)**
**Sintomas**: Muitos documentos em "Falhas"
**Soluções**:
1. Ajuste limite de confiança para 60%
2. Adicione palavras-chave específicas
3. Verifique se documentos têm nomes descritivos

#### 🐌 **Processamento lento**
**Sintomas**: Sistema demora muito para processar
**Soluções**:
1. Reduza máximo de documentos para 50
2. Verifique conexão com OnBase
3. Aumente intervalo para 3 horas

#### 📧 **Não recebo relatórios**
**Sintomas**: Emails não chegam
**Soluções**:
1. Verifique configuração de email em `config.json`
2. Confirme com TI se servidor SMTP está funcionando
3. Verifique pasta de spam

### Códigos de Erro

| Código | Descrição | Solução |
|--------|-----------|---------|
| AUTH_001 | Falha na autenticação OnBase | Verifique usuário/senha |
| CONN_002 | Erro de conexão | Verifique internet |
| CLASS_003 | Erro na classificação | Documento sem informações claras |
| MOVE_004 | Erro ao mover documento | Verifique permissões OnBase |

### Quando Solicitar Suporte

Entre em contato com TI quando:
- Sistema não funciona após seguir soluções acima
- Taxa de sucesso permanece baixa por vários dias
- Relatórios mostram erros recorrentes
- Necessidade de adicionar novos setores

---

## 📞 Suporte

### Suporte Imediato

1. **Consulte este manual**: Maioria dos problemas têm solução aqui
2. **Verifique logs**: Log de atividades mostra o que está acontecendo
3. **Reinicie o sistema**: Para > Iniciar resolve muitos problemas

### Contato com TI

**Email**: ti@poupex.com.br  
**Assunto**: "[OnBase Automação] Descrição do problema"

**Inclua sempre**:
- Captura de tela do erro
- Horário que o problema ocorreu
- Estatísticas atuais do sistema
- Últimas entradas do log

### Horário de Suporte

- **Dias úteis**: 8h às 18h
- **Urgências**: Via telefone (informar extensão)
- **Finais de semana**: Sistema funciona automaticamente

### Atualizações do Sistema

- **Automáticas**: Sistema se atualiza sozinho
- **Manutenção**: Comunicada com antecedência
- **Novas funcionalidades**: Treinamento será fornecido

---

## 📊 Métricas de Sucesso

### Metas Operacionais

- **Taxa de Sucesso**: ≥ 90%
- **Tempo de Processamento**: < 5 segundos por documento
- **Disponibilidade**: ≥ 95% durante horário comercial
- **Documentos por Dia**: Capacidade para 1000+ documentos

### Indicadores de Performance

- **Verde (Excelente)**: Taxa ≥ 95%
- **Amarelo (Bom)**: Taxa 85-94%
- **Vermelho (Atenção)**: Taxa < 85%

### Relatórios Gerenciais

Disponíveis mensalmente:
- Produtividade por setor
- Tendências de volume
- Evolução da precisão
- ROI da automação

---

**Desenvolvido especialmente para POUPEX FHE**  
*Sistema de Automação Inteligente v1.0*

---

*Este manual foi criado para facilitar o uso do sistema por qualquer pessoa, independente do conhecimento técnico. Em caso de dúvidas, sempre entre em contato com a equipe de TI.*