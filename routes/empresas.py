from flask import Blueprint, flash, render_template, request, redirect, url_for
from database import conectar_banco
import sqlite3 


# Criamos o Blueprint
bp_empresas = Blueprint('empresas', __name__)



from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar_banco
import sqlite3 

# Criamos o Blueprint
bp_empresas = Blueprint('empresas', __name__)


@bp_empresas.route('/cadastros', methods=['POST'])
def cadastrar_empresa():

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
        
        flash("Empresa cadastrada com sucesso!", "sucesso")
        return redirect('/')

    except sqlite3.IntegrityError:
        conn.close()
        flash("E-mail ou CNPJ já cadastrado!", "erro")
        return redirect('/')