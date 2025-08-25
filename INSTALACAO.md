
# 🚀 Guia de Instalação - Banco Luis & Machado

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## ⚡ Instalação Rápida

### Método 1: Automático
```bash
python setup.py
```

### Método 2: Manual
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar o sistema
python app.py
```

### Método 3: Script de Execução
```bash
python run.py
```

## 📁 Estrutura do Projeto

```
banco-luis-machado/
├── 📄 app.py              # Aplicação principal Flask
├── 📄 database.py         # Configuração do banco SQLite
├── 📄 setup.py           # Script de instalação
├── 📄 run.py             # Script para executar
├── 📄 requirements.txt    # Dependências Python
├── 📄 README.md          # Documentação
├── 📄 INSTALACAO.md      # Este arquivo
├── 📄 .gitignore         # Arquivos a ignorar no Git
├── 📁 static/
│   └── 📄 style.css      # Estilos CSS
└── 📁 templates/
    ├── 📄 base.html      # Template base
    ├── 📄 index.html     # Página inicial
    ├── 📄 login.html     # Página de login
    ├── 📄 register.html  # Página de registro
    ├── 📄 dashboard.html # Dashboard principal
    └── 📄 transferir.html # Página de transferência
```

## 🎯 Funcionalidades

- ✅ Registro de usuários (inicia com 0 coins)
- ✅ Sistema de login seguro
- ✅ Dashboard com saldo em tempo real
- ✅ Transferências entre usuários
- ✅ Sistema de créditos
- ✅ Histórico de transações
- ✅ Banco de dados SQLite persistente
- ✅ Interface responsiva e moderna

## 🔧 Comandos Úteis

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar em modo desenvolvimento
python app.py

# Executar com script helper
python run.py

# Configurar projeto (primeira vez)
python setup.py
```