"""
Legacy controllers facade module for backward compatibility.
Delegates functions to refactored controllers in controllers/ and services/.
"""
from controllers.product_controller import (
    listar_produtos,
    buscar_produto,
    criar_produto,
    atualizar_produto,
    deletar_produto,
    buscar_produtos
)
from controllers.user_controller import (
    listar_usuarios,
    buscar_usuario,
    criar_usuario,
    login
)
from controllers.order_controller import (
    criar_pedido,
    listar_pedidos_usuario,
    listar_todos_pedidos,
    atualizar_status_pedido
)
from controllers.report_controller import (
    relatorio_vendas
)
from controllers.admin_controller import (
    health_check,
    reset_database,
    executar_query
)
