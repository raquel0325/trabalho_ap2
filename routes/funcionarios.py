from flask import Blueprint, flash, render_template, request, redirect, url_for
from database import conectar_banco
import sqlite3 


# Criamos o Blueprint
bp_funcionarios = Blueprint('funcionarios', __name__)


@bp_funcionarios.route('/cadastro', methods=['POST'])
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


        return redirect(url_for('questionario.questionario_pag', id_func=id_new_employer))
        
    except sqlite3.IntegrityError:
        conn.close()
        flash("E-mail ou CNPJ já cadastrado!", "erro")
        return redirect('/')
    

