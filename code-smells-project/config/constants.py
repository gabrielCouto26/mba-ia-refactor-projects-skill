"""Business domain constants and static definitions."""

VALID_CATEGORIES = [
    "informatica",
    "moveis",
    "vestuario",
    "geral",
    "eletronicos",
    "livros"
]

VALID_ORDER_STATUSES = [
    "pendente",
    "aprovado",
    "enviado",
    "entregue",
    "cancelado"
]

PRODUCT_NAME_MIN_LENGTH = 2
PRODUCT_NAME_MAX_LENGTH = 200

# Discount calculation tiers for sales report
DISCOUNT_TIERS = [
    {"min_revenue": 10000.0, "rate": 0.10},
    {"min_revenue": 5000.0, "rate": 0.05},
    {"min_revenue": 1000.0, "rate": 0.02},
]
