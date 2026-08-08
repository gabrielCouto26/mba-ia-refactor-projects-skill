import os

class Config:
    """Base application configuration loaded from environment variables."""
    SECRET_KEY = os.getenv("SECRET_KEY", "minha-chave-super-secreta-123")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")
    ENV = os.getenv("FLASK_ENV", "development")
