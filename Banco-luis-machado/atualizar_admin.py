import os
import shutil

def backup_arquivos():
    """Faz backup dos arquivos atuais"""
    if os.path.exists('app.py'):
        shutil.copy('app.py', 'app_backup.py')
        print("📋 Backup do app.py criado")

def substituir_app_py():
    """Substitui o app.py atual"""
    print("🔄 Substituindo app.py...")
    # Como o novo código está no primeiro artefato, vamos apenas avisar
    print("✅ Copie o código do primeiro artefato para seu app.py")

def criar_template_admin():
    """Cria o template admin.html"""
    admin_html = '''{% extends "base.html" %}

{% block title %}Painel Admin - Banco Luis & Machado{% endblock %}

{% block content %}
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
        👑 Painel Administrativo
    </h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">
        Bem-vindo, {{ session.user_nome }}!
    </p>
</div>

<!-- Estatísticas -->
<div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); margin-bottom: 2rem;">
    <div class="card" style="text-align: center; background: linear-gradient(45deg, #667eea, #764ba2); color: white;">
        <h3 style="margin-bottom: 1rem;">👥 Usuários</h3>
        <div style="font-size: 2.5rem; font-weight: bold;">{{ stats.total_usuarios }}</div>
        <p style="opacity: 0.9;">Total de contas</p>
    </div>
    <div class="card" style="text-align: center; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); color: white;">
        <h3 style="margin-bottom: 1rem;">💰 Coins</h3>
        <div style="font-size: 2.5rem; font-weight: bold;">{{ "%.0f"|format(stats.total_coins) }}</div>
        <p style="opacity: 0.9;">Total em circulação</p>
    </div>
    <div class="card" style="text-align: center; background: linear-gradient(45deg, #4ecdc4, #44a08d); color: white;">
        <h3 style="margin-bottom: 1rem;">📊 Transações</h3>
        <div style="font-size: 2.5rem; font-weight: bold;">{{ stats.total_transacoes }}</div>
        <p style="opacity: 0.9;">Total realizadas</p>
    </div>
</div>

<div class="grid">
    <!-- Gerenciar Usuários -->
    <div class="card">
        <h3 style="margin-bottom: 1.5rem; color: #333;">👥 Gerenciar Usuários</h3>
        <div style="max-height: 400px; overflow-y: auto;">
            {% for usuario in usuarios %}
            <div class="transacao-item" style="border-bottom: 1px solid #eee; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-weight: bold;">{{ usuario.nome }}</div>
                    <div style="font-size: 0.9rem; color: #666;">{{ usuario.email }}</div>
                    <div style="font-size: 0.9rem; color: #888;">Cadastrado: {{ usuario.data_criacao[:10] }}</div>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div class="valor-positivo">{{ "%.2f"|format(usuario.saldo) }} coins</div>
                    <button onclick="adicionarCreditoUsuario({{ usuario.id }}, '{{ usuario.nome }}')" 
                            class="btn" style="padding: 8px 12px; font-size: 0.9rem;">
                        💳 Crédito
                    </button>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <!-- Últimas Transações -->
    <div class="card">
        <h3 style="margin-bottom: 1.5rem; color: #333;">📊 Últimas Transações</h3>
        <div style="max-height: 400px; overflow-y: auto;">
            {% if transacoes %}
                {% for transacao in transacoes %}
                <div class="transacao-item">
                    <div>
                        <div style="font-weight: bold; margin-bottom: 0.3rem;">
                            {% if transacao.tipo == 'credito_admin' %}
                                👑 Crédito Admin → {{ transacao.destino_nome }}
                            {% elif transacao.tipo == 'credito' %}
                                💰 Crédito → {{ transacao.destino_nome }}
                            {% elif transacao.tipo == 'transferencia' %}
                                💸 {{ transacao.origem_nome }} → {{ transacao.destino_nome }}
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
                    <div class="valor-positivo">
                        {{ "%.2f"|format(transacao.valor) }} coins
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div style="text-align: center; padding: 2rem; color: #666;">
                    <p>Nenhuma transação ainda</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>

<script>
function adicionarCreditoUsuario(userId, userName) {
    const valor = prompt(`💰 Quanto crédito adicionar para ${userName}? (em coins)`);
    if (valor && !isNaN(valor) && parseFloat(valor) > 0) {
        fetch('/admin/adicionar_credito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'user_id=' + userId + '&valor=' + encodeURIComponent(valor)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('🎉 ' + data.message);
                location.reload();
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
    
    with open('templates/admin.html', 'w', encoding='utf-8') as f:
        f.write(admin_html)
    print("✅ templates/admin.html criado!")

def atualizar_dashboard():
    """Atualiza o dashboard removendo botão de crédito"""
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
    <div style="margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
        <p style="font-size: 0.9rem; opacity: 0.9;">
            🔒 Apenas administradores podem adicionar créditos
        </p>
    </div>
</div>

<div class="grid">
    <div class="card">
        <h3 style="margin-bottom: 1.5rem; color: #333;">
            🚀 Ações Disponíveis
        </h3>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <a href="{{ url_for('transferir') }}" class="btn">
                💸 Transferir Coins
            </a>
            <button class="btn" onclick="location.reload()" style="background: linear-gradient(45deg, #4ecdc4, #44a08d);">
                🔄 Atualizar Dados
            </button>
            <div style="padding: 1rem; background: rgba(255, 193, 7, 0.1); border-radius: 10px; border-left: 4px solid #ffc107; margin-top: 1rem;">
                <p style="font-size: 0.9rem; color: #856404; margin: 0;">
                    💡 <strong>Dica:</strong> Para receber coins, peça para alguém transferir para você ou solicite crédito ao administrador!
                </p>
            </div>
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
                            {% if transacao.tipo == 'credito_admin' %}
                                👑 Crédito do Admin
                            {% elif transacao.tipo == 'credito' %}
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
{% endblock %}
'''
    
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    print("✅ templates/dashboard.html atualizado!")

def atualizar_base_template():
    """Atualiza o template base para incluir navegação admin"""
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
                {% if session.is_admin %}
                <div class="nav-links">
                    <a href="{{ url_for('admin_panel') }}">👑 Admin</a>
                    <a href="{{ url_for('logout') }}">👋 Sair</a>
                </div>
                {% else %}
                <div class="nav-links">
                    <a href="{{ url_for('dashboard') }}">🏠 Dashboard</a>
                    <a href="{{ url_for('transferir') }}">💸 Transferir</a>
                    <a href="{{ url_for('logout') }}">👋 Sair</a>
                </div>
                {% endif %}
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
    print("✅ templates/base.html atualizado!")

def main():
    print("👑 ATUALIZANDO SISTEMA COM FUNCIONALIDADES ADMIN")
    print("=" * 50)
    print("🔑 Admin: 1337metasploit@gmail.com")
    print("🔒 Senha: Lm99626731###")
    print("=" * 50)
    
    try:
        backup_arquivos()
        criar_template_admin()
        atualizar_dashboard()
        atualizar_base_template()
        
        print("\n🎉 ATUALIZAÇÃO CONCLUÍDA!")
        print("=" * 30)
        print("⚠️ IMPORTANTE: Substitua seu app.py atual pelo código do primeiro artefato!")
        print("✅ Templates atualizados")
        print("👑 Sistema admin configurado")
        print("🚀 Execute: python app.py")
        print("=" * 30)
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()