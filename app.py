from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import random
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://advinha_db_user:g5HLgah5N152Oy6R5PPYGS9GkdTSQJyY@dpg-cvemilt2ng1s73chu6g0-a.oregon-postgres.render.com/advinha_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Configura a migração
from models import *  # Certifique-se de que suas tabelas estão importadas
app.config.from_object(Config)

@app.route('/')
def index():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
    
    try:
        user_guess = int(request.form['guess'])
    except ValueError:
        flash("Por favor, insira um número válido.", "danger")
        return redirect(url_for('index'))
    
    number = session['number']
    
    if user_guess < number:
        flash("Muito baixo! Tente novamente.", "warning")
    elif user_guess > number:
        flash("Muito alto! Tente novamente.", "warning")
    else:
        flash("Parabéns! Você acertou! Um novo número foi gerado.", "success")
        session['number'] = random.randint(1, 100)
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                user.score += 1
                db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        if User.query.filter_by(username=username).first():
            flash("Usuário já existe!", "danger")
            return redirect(url_for('register'))
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login bem-sucedido!", "success")
            return redirect(url_for('index'))
        else:
            flash("Usuário ou senha inválidos!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for('index'))

@app.route('/ranking')
def ranking():
    top_users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template('ranking.html', top_users=top_users)

if __name__ == '__main__':
    app.run(debug=True)
