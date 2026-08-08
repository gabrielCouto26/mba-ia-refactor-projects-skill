from flask import Blueprint
import controllers.order_controller as order_controller

order_bp = Blueprint("orders", __name__)

order_bp.add_url_rule("/pedidos", "criar_pedido", order_controller.criar_pedido, methods=["POST"])
order_bp.add_url_rule("/pedidos", "listar_todos_pedidos", order_controller.listar_todos_pedidos, methods=["GET"])
order_bp.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", order_controller.listar_pedidos_usuario, methods=["GET"])
order_bp.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status_pedido", order_controller.atualizar_status_pedido, methods=["PUT"])
