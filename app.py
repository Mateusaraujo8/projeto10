from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para usar sessão

def iniciar_jogo():
    """Inicia um novo jogo e reseta as variáveis da sessão, mantendo o nome."""
    session['numero_secreto'] = random.randint(1, 100)
    session['tentativas'] = 0
    session['mensagem'] = "Tente adivinhar um número entre 1 e 100."

    # Garante que o histórico e o nome do usuário sejam mantidos
    session.setdefault('historico', [])
    session.setdefault('nome', None)

@app.route("/", methods=["GET", "POST"])
def pedir_nome():
    """Página inicial para pedir o nome do jogador."""
    if request.method == "POST":
        nome = request.form.get("nome").strip()
        if nome:
            session['nome'] = nome  # Salva o nome na sessão
            iniciar_jogo()  # Inicia o jogo depois de salvar o nome
            return redirect(url_for("index"))
    return render_template("nome.html")

@app.route("/jogo", methods=["GET", "POST"])
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
                
                # Garante que o histórico tenha o nome correto
                session['historico'].append({
                    "nome": session.get('nome', 'Jogador'),
                    "tentativas": session['tentativas'],
                    "numero_secreto": session['numero_secreto']
                })

                return redirect(url_for("novo_jogo"))
        except ValueError:
            session['mensagem'] = "Por favor, digite um número válido."

    return render_template("index.html", mensagem=session['mensagem'], 
                           tentativas=session['tentativas'], 
                           historico=session['historico'], 
                           nome=session['nome'])


@app.route("/novo")
def novo_jogo():
    """Reinicia o jogo, mas mantém o nome e o histórico."""
    nome = session.get('nome', None)  # Guarda o nome antes de reiniciar
    iniciar_jogo()
    session['nome'] = nome  # Restaura o nome do jogador
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
