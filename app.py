from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Alterar por uma chave segura

@app.route("/", methods=["GET", "POST"])
def index():
    """Rota principal do jogo."""
    if 'nome' not in session:
        return redirect(url_for("pedir_nome"))

    if request.method == "POST":
        try:
            palpite = int(request.form["palpite"])
            session['tentativas'] += 1

            if palpite < session['numero_secreto']:
                session['mensagem'] = "Muito baixo! Tente um número maior."
            elif palpite > session['numero_secreto']:
                session['mensagem'] = "Muito alto! Tente um número menor."
            else:
                session['mensagem'] = f"Parabéns, {session['nome']}! Você acertou em {session['tentativas']} tentativas."
                session['historico'].append({
                    "nome": session['nome'],
                    "tentativas": session['tentativas'],
                    "numero_secreto": session['numero_secreto']
                })
                return redirect(url_for("novo_jogo"))
        except ValueError:
            session['mensagem'] = "Por favor, digite um número válido."

    return render_template("index.html", mensagem=session['mensagem'],
                           tentativas=session['tentativas'],
                           historico=session['historico'], nome=session['nome'])

@app.route("/novo", methods=["GET"])
def novo_jogo():
    """Inicia um novo jogo."""
    session['numero_secreto'] = random.randint(1, 100)
    session['tentativas'] = 0
    return redirect(url_for('index'))

@app.route("/pedir_nome", methods=["GET", "POST"])
def pedir_nome():
    """Pede o nome do usuário."""
    if request.method == "POST":
        session['nome'] = request.form["nome"]
        session['historico'] = []
        return redirect(url_for("index"))
    return render_template("pedir_nome.html")

if __name__ == "__main__":
    app.run(debug=True)
