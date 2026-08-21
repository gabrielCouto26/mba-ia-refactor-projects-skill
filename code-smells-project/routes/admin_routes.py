from flask import Blueprint, request, jsonify, current_app
import controllers.admin_controller as admin_controller

admin_bp = Blueprint("admin", __name__)

@admin_bp.before_request
def require_admin_credentials():
	authorization = request.authorization
	configured_username = current_app.config.get("ADMIN_USERNAME")
	configured_password = current_app.config.get("ADMIN_PASSWORD")
	if not configured_username or not configured_password:
		return jsonify({"erro": "Administração não configurada"}), 503
	if not authorization or authorization.username != configured_username or authorization.password != configured_password:
		return jsonify({"erro": "Autenticação administrativa necessária"}), 401

admin_bp.add_url_rule("/admin/reset-db", "reset_database", admin_controller.reset_database, methods=["POST"])
