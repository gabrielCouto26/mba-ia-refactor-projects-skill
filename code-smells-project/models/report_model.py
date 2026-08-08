from database import get_db

def get_relatorio_vendas_data():
    """Retrieve raw aggregation metrics from database for sales reporting."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(total) FROM pedidos")
    faturamento = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
    pendentes = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
    aprovados = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
    cancelados = cursor.fetchone()[0] or 0

    return {
        "total_pedidos": total_pedidos,
        "faturamento": faturamento,
        "pendentes": pendentes,
        "aprovados": aprovados,
        "cancelados": cancelados
    }
