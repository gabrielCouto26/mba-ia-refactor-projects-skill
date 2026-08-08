from flask import Blueprint
import controllers.product_controller as product_controller

product_bp = Blueprint("products", __name__)

product_bp.add_url_rule("/produtos", "listar_produtos", product_controller.listar_produtos, methods=["GET"])
product_bp.add_url_rule("/produtos/busca", "buscar_produtos", product_controller.buscar_produtos, methods=["GET"])
product_bp.add_url_rule("/produtos/<int:id>", "buscar_produto", product_controller.buscar_produto, methods=["GET"])
product_bp.add_url_rule("/produtos", "criar_produto", product_controller.criar_produto, methods=["POST"])
product_bp.add_url_rule("/produtos/<int:id>", "atualizar_produto", product_controller.atualizar_produto, methods=["PUT"])
product_bp.add_url_rule("/produtos/<int:id>", "deletar_produto", product_controller.deletar_produto, methods=["DELETE"])
