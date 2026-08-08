from flask import request, jsonify
import services.user_service as user_service

def listar_usuarios():
    usuarios = user_service.listar_todos_usuarios()
    return jsonify({"dados": usuarios, "sucesso": True}), 200

def buscar_usuario(id):
    usuario = user_service.buscar_usuario_por_id(id)
    return jsonify({"dados": usuario, "sucesso": True}), 200

def criar_usuario():
    dados = request.get_json()
    user_id = user_service.cadastrar_usuario(dados)
    return jsonify({"dados": {"id": user_id}, "sucesso": True}), 201

def login():
    dados = request.get_json()
    usuario = user_service.autenticar_usuario(dados)
    return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
