from flask import Blueprint
import controllers.user_controller as user_controller

user_bp = Blueprint("users", __name__)

user_bp.add_url_rule("/usuarios", "listar_usuarios", user_controller.listar_usuarios, methods=["GET"])
user_bp.add_url_rule("/usuarios/<int:id>", "buscar_usuario", user_controller.buscar_usuario, methods=["GET"])
user_bp.add_url_rule("/usuarios", "criar_usuario", user_controller.criar_usuario, methods=["POST"])
user_bp.add_url_rule("/login", "login", user_controller.login, methods=["POST"])
