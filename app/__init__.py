from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Database mock (substitua por um banco real)
users = {}

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Função para checar se o usuário está logado
def is_logged_in():
    return 'user' in session


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['user'] = username  # Armazena o nome de usuário na sessão
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Usuário já registrado', 'warning')
        else:
            # Armazenar a senha criptografada
            hashed_password = generate_password_hash(password)
            users[username] = hashed_password
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/home')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    return f'Bem-vindo, {session["user"]}!'


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
