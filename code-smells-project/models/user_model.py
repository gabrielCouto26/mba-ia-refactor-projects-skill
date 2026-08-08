from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def row_to_dict(row, include_password=False):
    if not row:
        return None
    data = {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"]
    }
    if include_password:
        data["senha"] = row["senha"]
    return data

def get_todos_usuarios():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    return [row_to_dict(row, include_password=True) for row in rows]

def get_usuario_por_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return row_to_dict(row, include_password=True)

def get_usuario_por_email(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    return row

def login_usuario(email, senha):
    row = get_usuario_por_email(email)
    if not row:
        return None

    stored_password = row["senha"]
    # Check hashed password or fallback to plaintext comparison for legacy compatibility
    is_valid = False
    if stored_password.startswith("pbkdf2:") or stored_password.startswith("scrypt:"):
        is_valid = check_password_hash(stored_password, senha)
    else:
        is_valid = (stored_password == senha)

    if is_valid:
        return row_to_dict(row)
    return None

def criar_usuario(nome, email, senha, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    hashed_password = generate_password_hash(senha, method="pbkdf2:sha256")
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, hashed_password, tipo)
    )
    db.commit()
    return cursor.lastrowid
