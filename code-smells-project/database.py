import sqlite3
from flask import g
from config import Config
from werkzeug.security import generate_password_hash

def get_db():
    """Retrieve or initialize a request-scoped database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
        init_db_schema(g.db)
    return g.db

def close_db(e=None):
    """Close the request-scoped database connection on application context teardown."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db_schema(db):
    """Ensure database schema tables exist and seed initial data if empty."""
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            ativo INTEGER DEFAULT 1,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT DEFAULT 'cliente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pendente',
            total REAL NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)
    db.commit()

    cursor.execute("SELECT COUNT(*) FROM produtos")
    if cursor.fetchone()[0] == 0:
        produtos = [
            ("Notebook Gamer", "Notebook potente para jogos", 5999.99, 10, "informatica"),
            ("Mouse Wireless", "Mouse sem fio ergonômico", 89.90, 50, "informatica"),
            ("Teclado Mecânico", "Teclado mecânico RGB", 299.90, 30, "informatica"),
            ("Monitor 27''", "Monitor 27 polegadas 144hz", 1899.90, 15, "informatica"),
            ("Headset Gamer", "Headset com microfone", 199.90, 25, "informatica"),
            ("Cadeira Gamer", "Cadeira ergonômica", 1299.90, 8, "moveis"),
            ("Webcam HD", "Webcam 1080p", 249.90, 20, "informatica"),
            ("Hub USB", "Hub USB 3.0 7 portas", 79.90, 40, "informatica"),
            ("SSD 1TB", "SSD NVMe 1TB", 449.90, 35, "informatica"),
            ("Camiseta Dev", "Camiseta estampa código", 59.90, 100, "vestuario"),
        ]
        cursor.executemany(
            "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
            produtos
        )

        usuarios = [
            ("Admin", "admin@loja.com", generate_password_hash("admin123", method="pbkdf2:sha256"), "admin"),
            ("João Silva", "joao@email.com", generate_password_hash("123456", method="pbkdf2:sha256"), "cliente"),
            ("Maria Santos", "maria@email.com", generate_password_hash("senha123", method="pbkdf2:sha256"), "cliente"),
        ]
        cursor.executemany(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            usuarios
        )
        db.commit()
