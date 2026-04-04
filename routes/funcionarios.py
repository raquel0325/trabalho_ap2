from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar_banco
import sqlite3 


# Criamos o Blueprint
bp_funcionarios = Blueprint('funcionarios', __name__)


@bp_funcionarios.route('/cadastro/funcionario', methods=['POST'])
def cadastro_funcionario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')
    cpf = request.form.get('cpf')

    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO funcionarios (nome, email, senha, telefone, cpf)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, senha, telefone, cpf))
        
        id_new_employer = cursor.lastrowid # Pega o ID gerado
        conn.commit()
        conn.close()

        #  nome_do_blueprint.nome_da_funcao
        return redirect(url_for('funcionarios.questionario_pag', id_func=id_new_employer))
        
    except sqlite3.IntegrityError:
        conn.close()
        return "Erro: CPF ou E-mail já cadastrado!", 400

@bp_funcionarios.route('/questionario/funcionario/<int:id_func>')
def questionario_pag(id_func):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM competencias")
    comps = cursor.fetchall()
    conn.close()

    return render_template('questionario.html', id_func=id_func, competencias=comps)