from flask import Flask, render_template, request, session, redirect, url_for
from database import conectar_banco
import sqlite3
import os 

app = Flask(__name__)
app.secret_key = 'minha_chave_superhiper_mega_segura_123'

@app.route('/')
def pagina_cadastro():
    return render_template('index.html')

# Blueprints
from routes.funcionarios import bp_funcionarios
app.register_blueprint(bp_funcionarios)

from routes.empresas import bp_empresas
app.register_blueprint(bp_empresas)

from routes.login import bp_login
app.register_blueprint(bp_login)

from routes.questionario import bp_questionario_comp
app.register_blueprint(bp_questionario_comp)

from routes.home import bp_home 
app.register_blueprint(bp_home)

# Importar e inicializar o OAuth para Google
from routes.logincomgoogle import bp_google, init_oauth
init_oauth(app)
app.register_blueprint(bp_google)


if __name__ == '__main__':
    app.run(debug=True)