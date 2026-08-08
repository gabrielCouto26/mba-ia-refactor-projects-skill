import models.report_model as report_model
from config.constants import DISCOUNT_TIERS

def gerara_relatorio_vendas():
    raw_data = report_model.get_relatorio_vendas_data()
    faturamento = raw_data["faturamento"]
    total_pedidos = raw_data["total_pedidos"]

    desconto = 0.0
    for tier in DISCOUNT_TIERS:
        if faturamento > tier["min_revenue"]:
            desconto = faturamento * tier["rate"]
            break

    faturamento_bruto = round(faturamento, 2)
    desconto_aplicavel = round(desconto, 2)
    faturamento_liquido = round(faturamento - desconto, 2)
    ticket_medio = round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0.0

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": faturamento_bruto,
        "desconto_aplicavel": desconto_aplicavel,
        "faturamento_liquido": faturamento_liquido,
        "pedidos_pendentes": raw_data["pendentes"],
        "pedidos_aprovados": raw_data["aprovados"],
        "pedidos_cancelados": raw_data["cancelados"],
        "ticket_medio": ticket_medio
    }
