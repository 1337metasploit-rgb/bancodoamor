import sqlite3

DATABASE = 'banco_luis_machado.db'

def init_db():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            saldo REAL DEFAULT 0.0,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de transações
    cursor.execute('''
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
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!")

def get_db_connection():
    """Conecta ao banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn