from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Criação do banco de dados
db = SQLAlchemy()

# Inicializando o Login Manager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuração do aplicativo
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://advinha_db_8h7l_user:bmjqFV8cfmqdEePRM0jojm28M4hJH8qH@dpg-cvep0drtq21c73eghdcg-a/advinha_db_8h7l'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializando o banco de dados
    db.init_app(app)

    # Inicializando o Login Manager
    login_manager.init_app(app)

    # Mais configurações...

    return app
