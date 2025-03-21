from db import db

class Usuario(db.Model):
    __tablename__ = 'usuário'  # Define explicitamente o nome da tabela

    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
