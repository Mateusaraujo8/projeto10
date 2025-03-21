from app import create_app

# Criação da aplicação Flask
app = create_app()

# Inicia o servidor de desenvolvimento
if __name__ == "__main__":
    app.run(debug=True)
