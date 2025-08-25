import os

def criar_database_py():
    """Cria o arquivo database.py"""
    content = '''import sqlite3

DATABASE = 'banco_luis_machado.db'

def init_db():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            saldo REAL DEFAULT 0.0,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    \'\'\')
    
    # Tabela de transações
    cursor.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_origem INTEGER,
            usuario_destino INTEGER,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL,
            descricao TEXT,
            data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_origem) REFERENCES usuarios (id),
            FOREIGN KEY (usuario_destino) REFERENCES usuarios (id)
        )
    \'\'\')
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!")

def get_db_connection():
    """Conecta ao banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
'''
    with open('database.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ database.py criado!")

def criar_templates():
    """Cria todos os templates HTML"""
    os.makedirs('templates', exist_ok=True)
    
    # base.html
    base_html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Banco Luis & Machado{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💖</text></svg>">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">
                Banco Luis & Machado
            </div>
            {% if session.user_id %}
            <div class="nav-links">
                <a href="{{ url_for('dashboard') }}">🏠 Dashboard</a>
                <a href="{{ url_for('transferir') }}">💸 Transferir</a>
                <a href="{{ url_for('logout') }}">👋 Sair</a>
            </div>
            {% else %}
            <div class="nav-links">
                <a href="{{ url_for('login') }}">🔑 Entrar</a>
                <a href="{{ url_for('register') }}">✨ Cadastrar</a>
            </div>
            {% endif %}
        </div>
    </nav>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'success' if category == 'success' else 'error' }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
'''
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)
    
    # index.html
    index_html = '''{% extends "base.html" %}

{% block content %}
<div style="text-align: center; margin: 4rem auto; max-width: 800px;">
    <div class="card">
        <h1 class="hero-title">
            💖🌈 Bem-vindo ao Banco Luis & Machado!
        </h1>
        <p style="font-size: 1.3rem; margin-bottom: 2rem; color: #666;">
            O banco mais colorido e acolhedor do Brasil! 
            Gerencie seus coins com amor e segurança.
        </p>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <a href="{{ url_for('login') }}" class="btn">🔑 Fazer Login</a>
            <a href="{{ url_for('register') }}" class="btn">✨ Criar Conta</a>
        </div>
        
        <div style="margin-top: 3rem; padding: 1.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 15px;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">🎁 Comece Agora</h3>
            <p style="color: #666;">
                Crie sua conta e comece a usar nosso sistema de coins! 
                Cada novo usuário inicia com 0 coins, mas pode receber créditos facilmente.
            </p>
        </div>
    </div>
</div>
{% endblock %}
'''
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # register.html
    register_html = '''{% extends "base.html" %}

{% block title %}Cadastro - Banco Luis & Machado{% endblock %}

{% block content %}
<div class="card" style="max-width: 500px; margin: 2rem auto;">
    <h2 style="text-align: center; margin-bottom: 2rem; color: #333;">
        💖 Criar Nova Conta
    </h2>
    <form method="POST">
        <div class="form-group">
            <label for="nome">👤 Nome Completo:</label>
            <input type="text" id="nome" name="nome" required placeholder="Digite seu nome completo">
        </div>
        <div class="form-group">
            <label for="email">📧 Email:</label>
            <input type="email" id="email" name="email" required placeholder="seu@email.com">
        </div>
        <div class="form-group">
            <label for="senha">🔒 Senha:</label>
            <input type="password" id="senha" name="senha" required placeholder="Digite uma senha segura">
        </div>
        <button type="submit" class="btn" style="width: 100%;">
            ✨ Criar Minha Conta
        </button>
    </form>
    <div style="text-align: center; margin-top: 1.5rem;">
        <p style="color: #666;">
            Já tem conta? <a href="{{ url_for('login') }}" style="color: #4ecdc4; font-weight: bold;">Faça login aqui</a>
        </p>
    </div>
</div>
{% endblock %}
'''
    with open('templates/register.html', 'w', encoding='utf-8') as f:
        f.write(register_html)
    
    # login.html
    login_html = '''{% extends "base.html" %}

{% block title %}Login - Banco Luis & Machado{% endblock %}

{% block content %}
<div class="card" style="max-width: 500px; margin: 2rem auto;">
    <h2 style="text-align: center; margin-bottom: 2rem; color: #333;">
        🌈 Entrar na Conta
    </h2>
    <form method="POST">
        <div class="form-group">
            <label for="email">📧 Email:</label>
            <input type="email" id="email" name="email" required placeholder="seu@email.com">
        </div>
        <div class="form-group">
            <label for="senha">🔒 Senha:</label>
            <input type="password" id="senha" name="senha" required placeholder="Digite sua senha">
        </div>
        <button type="submit" class="btn" style="width: 100%;">
            🚀 Entrar
        </button>
    </form>
    <div style="text-align: center; margin-top: 1.5rem;">
        <p style="color: #666;">
            Não tem conta? <a href="{{ url_for('register') }}" style="color: #4ecdc4; font-weight: bold;">Cadastre-se gratuitamente</a>
        </p>
    </div>
</div>
{% endblock %}
'''
    with open('templates/login.html', 'w', encoding='utf-8') as f:
        f.write(login_html)
    
    # dashboard.html
    dashboard_html = '''{% extends "base.html" %}

{% block title %}Dashboard - Banco Luis & Machado{% endblock %}

{% block content %}
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
        Olá, {{ session.user_nome }}! 💖
    </h1>
</div>

<div class="saldo-display">
    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">💰 Seu Saldo Atual</div>
    <div class="saldo-valor" id="saldo-valor">{{ "%.2f"|format(saldo) }} coins</div>
    <button class="btn" onclick="adicionarCredito()" style="background: rgba(255,255,255,0.2); margin-top: 1rem; border: 2px solid rgba(255,255,255,0.3);">
        💳 Adicionar Crédito
    </button>
</div>

<div class="grid">
    <div class="card">
        <h3 style="margin-bottom: 1.5rem; color: #333;">
            🚀 Ações Rápidas
        </h3>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <a href="{{ url_for('transferir') }}" class="btn">
                💸 Transferir Coins
            </a>
            <button class="btn" onclick="location.reload()" style="background: linear-gradient(45deg, #4ecdc4, #44a08d);">
                🔄 Atualizar Dados
            </button>
        </div>
    </div>
    
    <div class="card">
        <h3 style="margin-bottom: 1.5rem; color: #333;">
            📊 Últimas Transações
        </h3>
        <div style="max-height: 400px; overflow-y: auto;">
            {% if transacoes %}
                {% for transacao in transacoes %}
                <div class="transacao-item">
                    <div>
                        <div style="font-weight: bold; margin-bottom: 0.3rem;">
                            {% if transacao.tipo == 'credito' %}
                                💰 Crédito Recebido
                            {% elif transacao.usuario_origem == session.user_id %}
                                📤 Enviado para: {{ transacao.destino_nome }}
                            {% else %}
                                📥 Recebido de: {{ transacao.origem_nome }}
                            {% endif %}
                        </div>
                        <div style="font-size: 0.9rem; color: #666;">
                            🕒 {{ transacao.data_transacao[:16] }}
                        </div>
                        {% if transacao.descricao %}
                        <div style="font-size: 0.9rem; color: #888; margin-top: 0.2rem;">
                            💬 {{ transacao.descricao }}
                        </div>
                        {% endif %}
                    </div>
                    <div class="{{ 'valor-positivo' if transacao.usuario_destino == session.user_id else 'valor-negativo' }}">
                        {{ '+' if transacao.usuario_destino == session.user_id else '-' }}{{ "%.2f"|format(transacao.valor) }} coins
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div style="text-align: center; padding: 2rem; color: #666;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
                    <p>Nenhuma transação ainda</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
                        Que tal fazer sua primeira transferência?
                    </p>
                </div>
            {% endif %}
        </div>
    </div>
</div>

<script>
function adicionarCredito() {
    const valor = prompt('💰 Quanto você gostaria de adicionar? (em coins)');
    if (valor && !isNaN(valor) && parseFloat(valor) > 0) {
        fetch('/receber_credito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'valor=' + encodeURIComponent(valor)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('saldo-valor').textContent = data.novo_saldo.toFixed(2) + ' coins';
                alert('🎉 ' + data.message);
                setTimeout(() => location.reload(), 1000);
            } else {
                alert('❌ ' + data.message);
            }
        })
        .catch(error => {
            alert('❌ Erro ao adicionar crédito');
        });
    } else if (valor !== null) {
        alert('⚠️ Por favor, digite um valor válido maior que zero!');
    }
}
</script>
{% endblock %}
'''
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    # transferir.html
    transferir_html = '''{% extends "base.html" %}

{% block title %}Transferir - Banco Luis & Machado{% endblock %}

{% block content %}
<div class="card" style="max-width: 600px; margin: 2rem auto;">
    <h2 style="text-align: center; margin-bottom: 2rem; color: #333;">
        💸 Transferir Coins
    </h2>
    
    <div style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
        <p>🏦 Transfira seus coins de forma segura e instantânea!</p>
    </div>
    
    <form method="POST" onsubmit="return confirmarTransferencia()">
        <div class="form-group">
            <label for="email_destino">📧 Email do Destinatário:</label>
            <input type="email" id="email_destino" name="email_destino" required 
                   placeholder="email@exemplo.com">
        </div>
        <div class="form-group">
            <label for="valor">💰 Valor (coins):</label>
            <input type="number" id="valor" name="valor" step="0.01" min="0.01" required 
                   placeholder="0.00">
        </div>
        <div class="form-group">
            <label for="descricao">💬 Descrição (opcional):</label>
            <input type="text" id="descricao" name="descricao" 
                   placeholder="Ex: Pagamento do almoço, Mesada, etc.">
        </div>
        <button type="submit" class="btn" style="width: 100%;">
            🚀 Realizar Transferência
        </button>
    </form>
    
    <div style="text-align: center; margin-top: 2rem;">
        <a href="{{ url_for('dashboard') }}" style="color: #4ecdc4; text-decoration: none; font-weight: bold;">
            ← 🏠 Voltar ao Dashboard
        </a>
    </div>
    
    <div style="margin-top: 2rem; padding: 1rem; background: rgba(255, 193, 7, 0.1); border-radius: 10px; border-left: 4px solid #ffc107;">
        <h4 style="color: #856404; margin-bottom: 0.5rem;">⚠️ Dicas de Segurança:</h4>
        <ul style="color: #856404; margin-left: 1rem;">
            <li>Verifique sempre o email do destinatário</li>
            <li>Confirme o valor antes de enviar</li>
            <li>Transferências não podem ser canceladas</li>
        </ul>
    </div>
</div>

<script>
function confirmarTransferencia() {
    const email = document.getElementById('email_destino').value;
    const valor = document.getElementById('valor').value;
    const descricao = document.getElementById('descricao').value;
    
    let mensagem = `🤔 Confirmar transferência?\\n\\n`;
    mensagem += `📧 Para: ${email}\\n`;
    mensagem += `💰 Valor: ${valor} coins\\n`;
    if (descricao) {
        mensagem += `💬 Descrição: ${descricao}\\n`;
    }
    mensagem += `\\n✅ Confirmar esta transferência?`;
    
    return confirm(mensagem);
}
</script>
{% endblock %}
'''
    with open('templates/transferir.html', 'w', encoding='utf-8') as f:
        f.write(transferir_html)
    
    print("✅ Todos os templates criados!")

def criar_css():
    """Cria o arquivo CSS"""
    os.makedirs('static', exist_ok=True)
    
    css_content = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.navbar {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 1rem 0;
    box-shadow: 0 2px 20px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
}

.logo {
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
}

.logo::before {
    content: "💖🌈";
    margin-right: 10px;
    font-size: 1.8rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-links a {
    text-decoration: none;
    color: #333;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.nav-links a:hover {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}

.btn {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
    text-align: center;
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    background: linear-gradient(45deg, #ff5252, #26a69a);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #555;
}

.form-group input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #ddd;
    border-radius: 10px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.9);
}

.form-group input:focus {
    outline: none;
    border-color: #4ecdc4;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
}

.alert {
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    font-weight: 500;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

.alert-success {
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background: linear-gradient(135deg, #f8d7da, #f5c6cb);
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.saldo-display {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    text-align: center;
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    position: relative;
    overflow: hidden;
}

.saldo-valor {
    font-size: 3.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.transacao-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #eee;
    transition: background 0.3s ease;
}

.transacao-item:hover {
    background: rgba(78, 205, 196, 0.1);
}

.transacao-item:last-child {
    border-bottom: none;
}

.valor-positivo {
    color: #28a745;
    font-weight: bold;
    font-size: 1.1rem;
}

.valor-negativo {
    color: #dc3545;
    font-weight: bold;
    font-size: 1.1rem;
}

.hero-title {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

@media (max-width: 768px) {
    .nav-container {
        flex-direction: column;
        gap: 1rem;
        padding: 0 1rem;
    }
    
    .hero-title {
        font-size: 2.5rem;
    }
    
    .saldo-valor {
        font-size: 2.5rem;
    }
    
    .container {
        padding: 1rem;
    }
}
'''
    with open('static/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("✅ CSS criado!")

def criar_requirements():
    """Cria o requirements.txt"""
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write("Flask==2.3.3\nWerkzeug==2.3.7\n")
    print("✅ requirements.txt criado!")

def main():
    print("🌈💖 RESOLVENDO PROJETO BANCO LUIS & MACHADO")
    print("=" * 50)
    
    try:
        criar_database_py()
        criar_templates()
        criar_css()
        criar_requirements()
        
        print("\n🎉 TUDO PRONTO!")
        print("=" * 30)
        print("✅ Todos os arquivos foram criados!")
        print("🚀 Agora execute: python app.py")
        print("📍 E acesse: http://localhost:5000")
        print("=" * 30)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("Tente executar como administrador ou verifique as permissões")

if __name__ == "__main__":
    main()