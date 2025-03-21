from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db, login_manager
from .models import User, Game
from .forms import RegistrationForm, LoginForm
import random

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.game'))
    return render_template('login.html', form=form)

@bp.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    game = Game.query.filter_by(user_id=current_user.id).first()
    if not game:
        target_number = random.randint(1, 100)
        game = Game(user_id=current_user.id, target_number=target_number)
        db.session.add(game)
        db.session.commit()

    result = None
    if request.method == 'POST':
        guess = int(request.form['guess'])
        if guess > game.target_number:
            result = "Muito alto!"
        elif guess < game.target_number:
            result = "Muito baixo!"
        else:
            result = "Correto! Você venceu!"
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('main.game'))

    return render_template('game.html', game=game, result=result)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
