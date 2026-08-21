import os

class Config:
    """Base application configuration loaded from environment variables."""
    SECRET_KEY = os.getenv("SECRET_KEY")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")
    ENV = os.getenv("FLASK_ENV", "development")
