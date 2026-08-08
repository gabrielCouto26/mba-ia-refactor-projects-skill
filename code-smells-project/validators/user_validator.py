from validators.product_validator import ValidationError

def validate_user_creation(dados):
    if not dados or not isinstance(dados, dict):
        raise ValidationError("Dados inválidos")

    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    senha = dados.get("senha", "").strip()

    if not nome or not email or not senha:
        raise ValidationError("Nome, email e senha são obrigatórios")

    return {"nome": nome, "email": email, "senha": senha}

def validate_login_payload(dados):
    if not dados or not isinstance(dados, dict):
        raise ValidationError("Dados inválidos")

    email = dados.get("email", "").strip()
    senha = dados.get("senha", "").strip()

    if not email or not senha:
        raise ValidationError("Email e senha são obrigatórios")

    return {"email": email, "senha": senha}
