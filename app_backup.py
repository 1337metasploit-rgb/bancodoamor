from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import hashlib
from functools import wraps
from database import init_db, get_db_connection

app = Flask(__name__)
app.secret_key = 'luis_machado_banco_secreto_2025'

# Credenciais do administrador
ADMIN_EMAIL = '1337metasploit@gmail.com'
ADMIN_PASSWORD = 'Lm99626731###'
ADMIN_NAME = 'ALEXANDRE DE MORAES'

def hash_password(password):
    """Criptografa a senha"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    """Decorator para verificar se o usuário está logado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator para verificar se o usuário é administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if not session.get('is_admin', False):
            flash('Acesso negado! Apenas administradores podem acessar esta página.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def is_admin_user(email):
    """Verifica se o email é do administrador"""
    return email == ADMIN_EMAIL

def criar_admin_se_necessario():
    """Cria conta do administrador se não existir"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM usuarios WHERE email = ?', (ADMIN_EMAIL,))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, saldo) 
            VALUES (?, ?, ?, 0.0)
        ''', (ADMIN_NAME, ADMIN_EMAIL, hash_password(ADMIN_PASSWORD)))
        conn.commit()
        print("🔑 Conta de administrador criada!")
    
    conn.close()

@app.route('/')
def index():
    """Página inicial"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de usuário"""
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios!', 'error')
            return render_template('register.html')
        
        # Verifica se está tentando se registrar com email de admin
        if is_admin_user(email):
            flash('Este email está reservado para administradores.', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica se o email já existe
        cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
        if cursor.fetchone():
            flash('Email já cadastrado!', 'error')
            conn.close()
            return render_template('register.html')
        
        # Insere o novo usuário (inicia com 0 coins)
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, saldo) 
            VALUES (?, ?, ?, 0.0)
        ''', (nome, email, hash_password(senha)))
        
        conn.commit()
        conn.close()
        
        flash('Conta criada com sucesso! Você iniciou com 0 coins.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login do usuário"""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # Verifica login de admin
        if is_admin_user(email) and senha == ADMIN_PASSWORD:
            session['user_id'] = 999999  # ID especial para admin
            session['user_nome'] = ADMIN_NAME
            session['is_admin'] = True
            flash(f'Bem-vindo, {ADMIN_NAME}! 👑', 'success')
            return redirect(url_for('admin_panel'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?', 
                      (email, hash_password(senha)))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_nome'] = user['nome']
            session['is_admin'] = False
            flash(f'Bem-vindo de volta, {user["nome"]}! 💖', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    flash('Logout realizado com sucesso! 👋', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    # Se for admin, redireciona para painel admin
    if session.get('is_admin', False):
        return redirect(url_for('admin_panel'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Busca saldo atual
    cursor.execute('SELECT saldo FROM usuarios WHERE id = ?', (session['user_id'],))
    saldo = cursor.fetchone()['saldo']
    
    # Busca últimas transações
    cursor.execute('''
        SELECT t.*, u1.nome as origem_nome, u2.nome as destino_nome
        FROM transacoes t
        LEFT JOIN usuarios u1 ON t.usuario_origem = u1.id
        LEFT JOIN usuarios u2 ON t.usuario_destino = u2.id
        WHERE t.usuario_origem = ? OR t.usuario_destino = ?
        ORDER BY t.data_transacao DESC
        LIMIT 10
    ''', (session['user_id'], session['user_id']))
    
    transacoes = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', saldo=saldo, transacoes=transacoes)

@app.route('/admin')
@admin_required
def admin_panel():
    """Painel administrativo"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Estatísticas gerais
    cursor.execute('SELECT COUNT(*) as total_usuarios FROM usuarios')
    total_usuarios = cursor.fetchone()['total_usuarios']
    
    cursor.execute('SELECT SUM(saldo) as total_coins FROM usuarios')
    total_coins = cursor.fetchone()['total_coins'] or 0
    
    cursor.execute('SELECT COUNT(*) as total_transacoes FROM transacoes')
    total_transacoes = cursor.fetchone()['total_transacoes']
    
    # Lista de usuários
    cursor.execute('SELECT id, nome, email, saldo, data_criacao FROM usuarios ORDER BY data_criacao DESC')
    usuarios = cursor.fetchall()
    
    # Últimas transações
    cursor.execute('''
        SELECT t.*, u1.nome as origem_nome, u2.nome as destino_nome
        FROM transacoes t
        LEFT JOIN usuarios u1 ON t.usuario_origem = u1.id
        LEFT JOIN usuarios u2 ON t.usuario_destino = u2.id
        ORDER BY t.data_transacao DESC
        LIMIT 20
    ''')
    
    transacoes = cursor.fetchall()
    conn.close()
    
    stats = {
        'total_usuarios': total_usuarios,
        'total_coins': total_coins,
        'total_transacoes': total_transacoes
    }
    
    return render_template('admin.html', stats=stats, usuarios=usuarios, transacoes=transacoes)

@app.route('/admin/adicionar_credito', methods=['POST'])
@admin_required
def admin_adicionar_credito():
    """Adiciona crédito a um usuário (apenas admin)"""
    user_id = int(request.form['user_id'])
    valor = float(request.form['valor'])
    
    if valor <= 0:
        return jsonify({'success': False, 'message': 'Valor deve ser maior que zero'})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Busca o usuário
        cursor.execute('SELECT nome FROM usuarios WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'success': False, 'message': 'Usuário não encontrado'})
        
        # Adiciona crédito
        cursor.execute('UPDATE usuarios SET saldo = saldo + ? WHERE id = ?', 
                      (valor, user_id))
        
        # Registra a transação
        cursor.execute('''
            INSERT INTO transacoes (usuario_destino, valor, tipo, descricao)
            VALUES (?, ?, 'credito_admin', 'Crédito adicionado pelo administrador')
        ''', (user_id, valor))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'{valor:.2f} coins adicionados para {user["nome"]}! 💰'
        })
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'success': False, 'message': 'Erro ao adicionar crédito'})

@app.route('/transferir', methods=['GET', 'POST'])
@login_required
def transferir():
    """Transferência entre usuários"""
    # Admin não pode fazer transferências normais
    if session.get('is_admin', False):
        flash('Administradores não podem fazer transferências. Use o painel admin para gerenciar créditos.', 'error')
        return redirect(url_for('admin_panel'))
    
    if request.method == 'POST':
        email_destino = request.form['email_destino']
        valor = float(request.form['valor'])
        descricao = request.form.get('descricao', '')
        
        if valor <= 0:
            flash('Valor deve ser maior que zero!', 'error')
            return render_template('transferir.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica saldo do usuário
        cursor.execute('SELECT saldo FROM usuarios WHERE id = ?', (session['user_id'],))
        saldo_atual = cursor.fetchone()['saldo']
        
        if saldo_atual < valor:
            flash('Saldo insuficiente!', 'error')
            conn.close()
            return render_template('transferir.html')
        
        # Busca usuário destino
        cursor.execute('SELECT id, nome FROM usuarios WHERE email = ?', (email_destino,))
        usuario_destino = cursor.fetchone()
        
        if not usuario_destino:
            flash('Usuário destinatário não encontrado!', 'error')
            conn.close()
            return render_template('transferir.html')
        
        if usuario_destino['id'] == session['user_id']:
            flash('Não é possível transferir para si mesmo!', 'error')
            conn.close()
            return render_template('transferir.html')
        
        # Não permite transferir para admin
        if email_destino == ADMIN_EMAIL:
            flash('Não é possível transferir para a conta administrativa!', 'error')
            conn.close()
            return render_template('transferir.html')
        
        # Realiza a transferência
        try:
            # Debita da conta origem
            cursor.execute('UPDATE usuarios SET saldo = saldo - ? WHERE id = ?', 
                         (valor, session['user_id']))
            
            # Credita na conta destino
            cursor.execute('UPDATE usuarios SET saldo = saldo + ? WHERE id = ?', 
                         (valor, usuario_destino['id']))
            
            # Registra a transação
            cursor.execute('''
                INSERT INTO transacoes (usuario_origem, usuario_destino, valor, tipo, descricao)
                VALUES (?, ?, ?, 'transferencia', ?)
            ''', (session['user_id'], usuario_destino['id'], valor, descricao))
            
            conn.commit()
            flash(f'Transferência de {valor:.2f} coins para {usuario_destino["nome"]} realizada com sucesso! 🎉', 'success')
            
        except Exception as e:
            conn.rollback()
            flash('Erro ao realizar transferência!', 'error')
        
        conn.close()
        return redirect(url_for('dashboard'))
    
    return render_template('transferir.html')

if __name__ == '__main__':
    # Inicializa banco de dados
    init_db()
    # Cria conta admin se necessário
    criar_admin_se_necessario()
    
    print("🌈💖 BANCO LUIS & MACHADO")
    print("=" * 40)
    print("🚀 Sistema iniciando...")
    print("📍 Acesse: http://localhost:5000")
    print("💰 Usuários iniciam com 0 coins")
    print("🔑 Admin: 1337metasploit@gmail.com")
    print("👑 Apenas admin pode adicionar créditos")
    print("=" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5000)