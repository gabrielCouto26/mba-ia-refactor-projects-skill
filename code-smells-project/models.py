"""
Legacy models facade module for backward compatibility.
Delegates functions to refactored models in models/.
"""
from models.product_model import (
    get_todos_produtos,
    get_produto_por_id,
    criar_produto,
    atualizar_produto,
    deletar_produto,
    buscar_produtos
)
from models.user_model import (
    get_todos_usuarios,
    get_usuario_por_id,
    login_usuario,
    criar_usuario
)
from models.order_model import (
    criar_pedido,
    get_pedidos_usuario,
    get_todos_pedidos,
    atualizar_status_pedido
)
from models.report_model import get_relatorio_vendas_data
from services.report_service import gerara_relatorio_vendas as relatorio_vendas
