from config.constants import VALID_CATEGORIES, PRODUCT_NAME_MIN_LENGTH, PRODUCT_NAME_MAX_LENGTH

class ValidationError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def validate_product_payload(dados, is_update=False):
    if not dados or not isinstance(dados, dict):
        raise ValidationError("Dados inválidos")

    if not is_update:
        if "nome" not in dados:
            raise ValidationError("Nome é obrigatório")
        if "preco" not in dados:
            raise ValidationError("Preço é obrigatório")
        if "estoque" not in dados:
            raise ValidationError("Estoque é obrigatório")

    nome = dados.get("nome")
    preco = dados.get("preco")
    estoque = dados.get("estoque")
    categoria = dados.get("categoria", "geral")

    if nome is not None:
        if not isinstance(nome, str) or len(nome) < PRODUCT_NAME_MIN_LENGTH:
            raise ValidationError("Nome muito curto")
        if len(nome) > PRODUCT_NAME_MAX_LENGTH:
            raise ValidationError("Nome muito longo")

    if preco is not None:
        if not isinstance(preco, (int, float)) or preco < 0:
            raise ValidationError("Preço não pode ser negativo")

    if estoque is not None:
        if not isinstance(estoque, int) or estoque < 0:
            raise ValidationError("Estoque não pode ser negativo")

    if categoria is not None:
        if categoria not in VALID_CATEGORIES:
            raise ValidationError(f"Categoria inválida. Válidas: {VALID_CATEGORIES}")

    return {
        "nome": nome,
        "descricao": dados.get("descricao", ""),
        "preco": preco,
        "estoque": estoque,
        "categoria": categoria
    }
