import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///tasks.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('true', '1')

    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

    JWT_SECRET = os.getenv('JWT_SECRET')

    @classmethod
    def validate(cls):
        if os.getenv('FLASK_ENV', 'development') == 'production':
            missing = [name for name in ('SECRET_KEY', 'JWT_SECRET') if not getattr(cls, name)]
            if missing:
                raise RuntimeError(f'Missing required production secrets: {", ".join(missing)}')
