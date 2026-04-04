from flask import Flask, render_template, request, session, redirect, url_for
from database import conectar_banco
import sqlite3
import os 

app = Flask(__name__)

app.secret_key = 'minha_chave_superhiper_mega_segura_123'

@app.route('/')
def pagina_cadastro():
    return render_template('index.html')

#============================================= cadastro funcionario ===============================================

from routes.funcionarios import bp_funcionarios
app.register_blueprint(bp_funcionarios)

#============================================= cadastro empresa ===============================================

from routes.empresas import bp_empresas
app.register_blueprint(bp_empresas)

#================================================== LOGIN ========================================

from routes.login import bp_login
app.register_blueprint(bp_login)

#=================================== QUESTIONARIO FUNCIONARIO ===================================

from routes.questionario import bp_questionario_comp
app.register_blueprint(bp_questionario_comp)




if __name__ == '__main__':
    
    app.run(debug=True)