import models.order_model as order_model
from validators.order_validator import validate_order_creation, validate_status_update
from validators.product_validator import ValidationError

def realizar_pedido(dados):
    validated_data = validate_order_creation(dados)
    resultado = order_model.criar_pedido(
        validated_data["usuario_id"],
        validated_data["itens"]
    )
    
    if "erro" in resultado:
        raise ValidationError(resultado["erro"], status_code=400)

    # Simulated notification side-effects
    print(f"ENVIANDO EMAIL: Pedido {resultado['pedido_id']} criado para usuario {validated_data['usuario_id']}")
    print("ENVIANDO SMS: Seu pedido foi recebido!")
    print("ENVIANDO PUSH: Novo pedido recebido pelo sistema")

    return resultado

def listar_pedidos_do_usuario(usuario_id):
    return order_model.get_pedidos_usuario(usuario_id)

def listar_todos_pedidos():
    return order_model.get_todos_pedidos()

def atualizar_status(pedido_id, dados):
    novo_status = validate_status_update(dados)
    success = order_model.atualizar_status_pedido(pedido_id, novo_status)
    if not success:
        raise ValidationError("Pedido não encontrado", status_code=404)

    if novo_status == "aprovado":
        print(f"NOTIFICAÇÃO: Pedido {pedido_id} foi aprovado! Preparar envio.")
    elif novo_status == "cancelado":
        print(f"NOTIFICAÇÃO: Pedido {pedido_id} cancelado. Devolver estoque.")

    return True
