from database import get_db

def _build_orders_from_join_rows(rows):
    """
    Assembles order dictionaries with nested item lists from SQL JOIN rows,
    resolving the N+1 query issue in a single pass.
    """
    orders_map = {}
    for row in rows:
        pedido_id = row["pedido_id"]
        if pedido_id not in orders_map:
            orders_map[pedido_id] = {
                "id": pedido_id,
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": []
            }
        
        if row["produto_id"] is not None:
            orders_map[pedido_id]["itens"].append({
                "produto_id": row["produto_id"],
                "produto_nome": row["produto_nome"] if row["produto_nome"] else "Desconhecido",
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"]
            })
            
    return list(orders_map.values())

def get_todos_pedidos():
    """Retrieve all orders and their items using a single JOIN query (eliminates N+1)."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            p.id AS pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
            ip.produto_id, ip.quantidade, ip.preco_unitario,
            pr.nome AS produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
        LEFT JOIN produtos pr ON ip.produto_id = pr.id
        ORDER BY p.id ASC
    """)
    rows = cursor.fetchall()
    return _build_orders_from_join_rows(rows)

def get_pedidos_usuario(usuario_id):
    """Retrieve orders for a specific user using a single JOIN query (eliminates N+1)."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            p.id AS pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
            ip.produto_id, ip.quantidade, ip.preco_unitario,
            pr.nome AS produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
        LEFT JOIN produtos pr ON ip.produto_id = pr.id
        WHERE p.usuario_id = ?
        ORDER BY p.id ASC
    """, (usuario_id,))
    rows = cursor.fetchall()
    return _build_orders_from_join_rows(rows)

def criar_pedido(usuario_id, itens):
    """
    Creates an order with line items and updates stock atomically using database transactions.
    """
    db = get_db()
    cursor = db.cursor()

    total = 0.0
    prepared_items = []

    # Batch validate items and calculate total
    for item in itens:
        produto_id = item["produto_id"]
        quantidade = item["quantidade"]
        
        cursor.execute("SELECT id, nome, preco, estoque FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()
        if produto is None:
            return {"erro": f"Produto {produto_id} não encontrado"}
        if produto["estoque"] < quantidade:
            return {"erro": f"Estoque insuficiente para {produto['nome']}"}
        
        preco_unitario = produto["preco"]
        total += preco_unitario * quantidade
        prepared_items.append((produto_id, quantidade, preco_unitario))

    # Insert order record
    cursor.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
        (usuario_id, total)
    )
    pedido_id = cursor.lastrowid

    # Bulk insert order items and update stock
    for produto_id, quantidade, preco_unitario in prepared_items:
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
            (pedido_id, produto_id, quantidade, preco_unitario)
        )
        cursor.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (quantidade, produto_id)
        )

    db.commit()
    return {"pedido_id": pedido_id, "total": total}

def atualizar_status_pedido(pedido_id, novo_status):
    """Updates order status using parameterized query."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (novo_status, pedido_id)
    )
    db.commit()
    return cursor.rowcount > 0
