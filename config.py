import os

class Config:
    # Pegando a chave secreta do ambiente ou definindo um valor padrão seguro
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_secreta_padrao')

    # Pegando a URL do banco de dados
    DATABASE_URL = os.environ.get('DATABASE_URL')

    # Corrigindo o prefixo 'postgres://' para 'postgresql://' (necessário para SQLAlchemy)
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Definindo a URI do banco de dados
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///fallback.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
