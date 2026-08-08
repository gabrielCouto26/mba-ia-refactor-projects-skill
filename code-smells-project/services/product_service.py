import models.product_model as product_model
from validators.product_validator import validate_product_payload, ValidationError

def listar_todos_produtos():
    return product_model.get_todos_produtos()

def buscar_produto_por_id(produto_id):
    produto = product_model.get_produto_por_id(produto_id)
    if not produto:
        raise ValidationError("Produto não encontrado", status_code=404)
    return produto

def criar_novo_produto(dados):
    validated_data = validate_product_payload(dados)
    product_id = product_model.criar_produto(
        validated_data["nome"],
        validated_data["descricao"],
        validated_data["preco"],
        validated_data["estoque"],
        validated_data["categoria"]
    )
    return product_id

def atualizar_produto_existente(produto_id, dados):
    produto_existente = product_model.get_produto_por_id(produto_id)
    if not produto_existente:
        raise ValidationError("Produto não encontrado", status_code=404)

    validated_data = validate_product_payload(dados, is_update=True)
    product_model.atualizar_produto(
        produto_id,
        validated_data["nome"],
        validated_data["descricao"],
        validated_data["preco"],
        validated_data["estoque"],
        validated_data["categoria"]
    )
    return True

def deletar_produto_por_id(produto_id):
    produto_existente = product_model.get_produto_por_id(produto_id)
    if not produto_existente:
        raise ValidationError("Produto não encontrado", status_code=404)

    product_model.deletar_produto(produto_id)
    return True

def pesquisar_produtos(termo, categoria=None, preco_min=None, preco_max=None):
    if preco_min is not None:
        try:
            preco_min = float(preco_min)
        except ValueError:
            raise ValidationError("preco_min inválido")
    if preco_max is not None:
        try:
            preco_max = float(preco_max)
        except ValueError:
            raise ValidationError("preco_max inválido")

    return product_model.buscar_produtos(termo, categoria, preco_min, preco_max)
