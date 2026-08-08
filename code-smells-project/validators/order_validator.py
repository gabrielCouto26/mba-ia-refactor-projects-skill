from config.constants import VALID_ORDER_STATUSES
from validators.product_validator import ValidationError

def validate_order_creation(dados):
    if not dados or not isinstance(dados, dict):
        raise ValidationError("Dados inválidos")

    usuario_id = dados.get("usuario_id")
    itens = dados.get("itens", [])

    if not usuario_id:
        raise ValidationError("Usuario ID é obrigatório")
    if not itens or not isinstance(itens, list) or len(itens) == 0:
        raise ValidationError("Pedido deve ter pelo menos 1 item")

    for item in itens:
        if not isinstance(item, dict) or "produto_id" not in item or "quantidade" not in item:
            raise ValidationError("Itens do pedido devem conter produto_id e quantidade")
        if not isinstance(item["quantidade"], int) or item["quantidade"] <= 0:
            raise ValidationError("Quantidade do item deve ser um inteiro positivo")

    return {"usuario_id": usuario_id, "itens": itens}

def validate_status_update(dados):
    if not dados or not isinstance(dados, dict):
        raise ValidationError("Dados inválidos")

    novo_status = dados.get("status", "")
    if novo_status not in VALID_ORDER_STATUSES:
        raise ValidationError("Status inválido")

    return novo_status
