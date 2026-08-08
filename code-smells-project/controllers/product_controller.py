from flask import request, jsonify
import services.product_service as product_service

def listar_produtos():
    produtos = product_service.listar_todos_produtos()
    return jsonify({"dados": produtos, "sucesso": True}), 200

def buscar_produto(id):
    produto = product_service.buscar_produto_por_id(id)
    return jsonify({"dados": produto, "sucesso": True}), 200

def criar_produto():
    dados = request.get_json()
    product_id = product_service.criar_novo_produto(dados)
    return jsonify({"dados": {"id": product_id}, "sucesso": True, "mensagem": "Produto criado"}), 201

def atualizar_produto(id):
    dados = request.get_json()
    product_service.atualizar_produto_existente(id, dados)
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

def deletar_produto(id):
    product_service.deletar_produto_por_id(id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200

def buscar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria", None)
    preco_min = request.args.get("preco_min", None)
    preco_max = request.args.get("preco_max", None)

    resultados = product_service.pesquisar_produtos(termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
