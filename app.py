from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import random
import os
from flask_migrate import Migrate

migrate = Migrate(app, db)

# No terminal, execute as migrações:
# flask db init
# flask db migrate
# flask db upgrade


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, default=0)

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
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
