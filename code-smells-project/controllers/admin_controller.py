from flask import jsonify, request, current_app
from database import get_db
from config import Config

def health_check():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    produtos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos = cursor.fetchone()[0]

    return jsonify({
        "status": "ok",
        "database": "connected",
        "counts": {
            "produtos": produtos,
            "usuarios": usuarios,
            "pedidos": pedidos
        },
        "versao": "1.0.0",
        "ambiente": Config.ENV
    }), 200

def reset_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200

def executar_query():
    # Restricted / Sanitized endpoint for administrative database queries
    dados = request.get_json() or {}
    query = dados.get("sql", "").strip()
    
    if not query:
        return jsonify({"erro": "Query não informada"}), 400

    # Block destructive/unauthorized SQL statements in raw query endpoint
    forbidden_keywords = ["DROP", "ALTER", "TRUNCATE"]
    if any(keyword in query.upper() for keyword in forbidden_keywords):
        return jsonify({"erro": "Comando SQL não permitido"}), 403

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query)
        if query.upper().startswith("SELECT"):
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            return jsonify({"dados": result, "sucesso": True}), 200
        else:
            db.commit()
            return jsonify({"mensagem": "Query executada", "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
