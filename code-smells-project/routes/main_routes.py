from flask import Blueprint, jsonify
import controllers.admin_controller as admin_controller

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health"
        }
    })

main_bp.add_url_rule("/health", "health_check", admin_controller.health_check, methods=["GET"])
