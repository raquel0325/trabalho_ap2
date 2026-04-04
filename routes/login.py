from flask import Blueprint, render_template, request, redirect, url_for, session 
from database import conectar_banco
import sqlite3 

# Criamos o Blueprint
bp_login = Blueprint('login', __name__)

@bp_login.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    conn = conectar_banco()
    cursor = conn.cursor()

    # 1. Busca nos funcionários
    cursor.execute('SELECT id_funcionario, nome FROM funcionarios WHERE email = ? AND senha = ?', (email, senha))
    funcionario = cursor.fetchone()

    if funcionario:
        session['usuario_id'] = funcionario[0]
        session['usuario_nome'] = funcionario[1]
        session['tipo'] = 'funcionario'
        conn.close()
        # Redirecionar  para o dashboard do funcionário
        return f"Bem-vindo Funcionário {funcionario[1]}!"

    # 2. Busca nas empresas
    cursor.execute('SELECT id_empresa, nome FROM empresas WHERE email = ? AND senha = ?', (email, senha))
    empresa = cursor.fetchone()

    if empresa:
        session['usuario_id'] = empresa[0]
        session['usuario_nome'] = empresa[1]
        session['tipo'] = 'empresa'
        conn.close()

        # Redirecionar para o dashboard da empresa
        return f"Bem-vindo Empresa {empresa[1]}!"

    conn.close()
    return "E-mail ou senha incorretos!", 401