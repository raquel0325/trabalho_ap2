from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar_banco
import sqlite3 


# Criamos o Blueprint
bp_empresas = Blueprint('empresas', __name__)



from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar_banco
import sqlite3 

# Criamos o Blueprint
bp_empresas = Blueprint('empresas', __name__)

# ATENÇÃO: Mudamos de @app para @bp_empresas
@bp_empresas.route('/cadastro/empresa', methods=['POST'])
def cadastrar_empresa():
    # Não precisa de "if request.method == 'POST'" se a rota só aceita POST, 
    # mas mantê-lo não faz mal.
    
    nome = request.form.get('nome')
    cnpj = request.form.get('cnpj')
    email = request.form.get('email')
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')
    
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO empresas (nome, cnpj, email, senha, telefone) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, cnpj, email, senha, telefone))
        
        conn.commit()
        conn.close()
        
        # Em vez de retornar apenas um texto, 
        # é melhor redirecionar para a página inicial ou login
        return "Empresa cadastrada com sucesso!" 

    except sqlite3.IntegrityError:
        conn.close()
        return "Erro: CNPJ ou E-mail já cadastrado!", 400