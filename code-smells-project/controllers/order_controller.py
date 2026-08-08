from flask import request, jsonify
import services.order_service as order_service

def criar_pedido():
    dados = request.get_json()
    resultado = order_service.realizar_pedido(dados)
    return jsonify({
        "dados": resultado,
        "sucesso": True,
        "mensagem": "Pedido criado com sucesso"
    }), 201

def listar_pedidos_usuario(usuario_id):
    pedidos = order_service.listar_pedidos_do_usuario(usuario_id)
    return jsonify({"dados": pedidos, "sucesso": True}), 200

def listar_todos_pedidos():
    pedidos = order_service.listar_todos_pedidos()
    return jsonify({"dados": pedidos, "sucesso": True}), 200

def atualizar_status_pedido(pedido_id):
    dados = request.get_json()
    order_service.atualizar_status(pedido_id, dados)
    return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200
