import models.user_model as user_model
from validators.user_validator import validate_user_creation, validate_login_payload
from validators.product_validator import ValidationError

def listar_todos_usuarios():
    return user_model.get_todos_usuarios()

def buscar_usuario_por_id(user_id):
    usuario = user_model.get_usuario_por_id(user_id)
    if not usuario:
        raise ValidationError("Usuário não encontrado", status_code=404)
    return usuario

def cadastrar_usuario(dados):
    validated_data = validate_user_creation(dados)
    
    # Check duplicate email
    existing_user = user_model.get_usuario_por_email(validated_data["email"])
    if existing_user:
        raise ValidationError("Email já cadastrado", status_code=400)

    user_id = user_model.criar_usuario(
        validated_data["nome"],
        validated_data["email"],
        validated_data["senha"]
    )
    return user_id

def autenticar_usuario(dados):
    validated_data = validate_login_payload(dados)
    usuario = user_model.login_usuario(
        validated_data["email"],
        validated_data["senha"]
    )
    if not usuario:
        raise ValidationError("Email ou senha inválidos", status_code=401)
    return usuario
