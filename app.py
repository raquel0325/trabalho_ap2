from flask import Flask, render_template, request, session, redirect, url_for

import sqlite3
import os 


app = Flask(__name__)

app.secret_key = 'minha_chave_superhiper_mega_segura_123'


def conectar_banco():
    conexao = sqlite3.connect('banco.db')
    return conexao




@app.route('/')

def pagina_cadastro():

    return render_template('index.html')

@app.route('/cadastro/funcionario', methods=['GET', 'POST'])
def cadastro_funcionario():
    if request.method == 'POST':
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
            conn.commit()
        except sqlite3.IntegrityError:
            return "Erro: CPF já cadastrado!"
        finally:
            conn.close()

            return "Funcionário cadastrado com sucesso!"
        

    return redirect('/')
    #return render_template('cadastro_funcionario.html')



@app.route('/cadastro/empresa', methods=['GET', 'POST'])
def cadastrar_empresa():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cnpj = request.form.get('cnpj')
        email = request.form.get('email')
        senha = request.form.get('senha')
        telefone = request.form.get('telefone')
        

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO empresas (nome, cnpj, email, senha, telefone) VALUES (?, ?, ?, ?, ?)', (nome, cnpj, email, senha, telefone))
        conn.commit()
        conn.close()
        return "Empresa cadastrada!"

    return redirect('/')
    #return render_template('cadastro_empresa.html')


@app.route('/login', methods=['POST'])

def login():
    email = request.form.get('email')
    senha = request.form.get('senha')


    #busca pelos funcionarios ou empreas
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('SELECT id_funcionario, nome FROM funcionarios WHERE email = ? AND senha = ?', (email, senha))
    funcionario = cursor.fetchone()

    if funcionario:
        session['usuario_id'] = funcionario[0]
        session['usuario_nome'] = funcionario[1]
        session['tipo'] = 'funcionario'
        conn.close()
        return f"Bem-vindo Funcionário {funcionario[1]}!"


    cursor.execute('SELECT id_empresa, nome FROM empresas WHERE email = ? AND senha = ?', (email, senha))
    empresa = cursor.fetchone()

    if empresa:
        session['usuario_id'] = empresa[0]
        session['usuario_nome'] = empresa[1]
        session['tipo'] = 'empresa'
        conn.close()
        return f"Bem-vindo Empresa {empresa[1]}!"

    conn.close()
    return "E-mail ou senha incorretos!", 401








if __name__ == '__main__':
    
    app.run(debug=True)