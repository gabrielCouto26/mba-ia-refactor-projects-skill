from flask import jsonify
import services.report_service as report_service

def relatorio_vendas():
    relatorio = report_service.gerara_relatorio_vendas()
    return jsonify({"dados": relatorio, "sucesso": True}), 200
