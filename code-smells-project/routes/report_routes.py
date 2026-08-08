from flask import Blueprint
import controllers.report_controller as report_controller

report_bp = Blueprint("reports", __name__)

report_bp.add_url_rule("/relatorios/vendas", "relatorio_vendas", report_controller.relatorio_vendas, methods=["GET"])
