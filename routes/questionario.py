from flask import Blueprint, flash, render_template, request, redirect, url_for, session 
from database import conectar_banco
import sqlite3 

# Criamos o Blueprint
bp_questionario_comp = Blueprint('questionario', __name__)

@bp_questionario_comp.route('/questionario/<int:id_func>')
def questionario_pag(id_func):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Busca as competências cadastradas para exibir no formulário
    cursor.execute("SELECT * FROM competencias")
    comps = cursor.fetchall()
    conn.close()
    return render_template('questionario.html', id_func=id_func, competencias=comps)
    



@bp_questionario_comp.route('/salvar_questionario', methods=['POST'])
def salvar_questionario():
    id_func = request.form.get('id_func')

    if 'usuario_id' not in session or session['usuario_id'] != int(id_func):
        flash("Sessão expirada. Por favor, faça login novamente!", "erro")
        return redirect('/')


    cidade = request.form.get('cidade')
    estado = request.form.get('estado')
    formacao = request.form.get('formacao')
    curso = request.form.get('curso')
    instituicao = request.form.get('instituicao')
    ano_conclusao = request.form.get('ano_conclusao')
    ultimo_cargo = request.form.get('ultimo_cargo')
    ultima_empresa = request.form.get('ultima_empresa')
    tempo_experiencia = request.form.get('tempo_experiencia')
    comps_existentes = request.form.getlist('competencias') # IDs (1, 2, 3...)
    lista_novas = request.form.getlist('novas_competencias') # Nomes (Photoshop, Inglês...)

    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        # 1. Inserir os dados do questionário principal
        cursor.execute("""
            INSERT INTO respostas_questionario 
            (id_funcionario, cidade, estado, formacao, curso, instituicao, 
             ano_conclusao, ultimo_cargo, ultima_empresa, tempo_experiencia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_func, cidade, estado, formacao, curso, instituicao, 
              ano_conclusao, ultimo_cargo, ultima_empresa, tempo_experiencia))
        
        # 2. Salvar competências existentes
        for comp_id in comps_existentes:
            cursor.execute("""
                INSERT OR IGNORE INTO funcionario_competencias 
                (id_funcionario, id_competencia) VALUES (?, ?)
            """, (id_func, comp_id))

        # 3. Salvar novas competências
        for nome_comp in lista_novas:
            # Verifica se já existe no banco geral
            cursor.execute("SELECT id_competencia FROM competencias WHERE nome = ?", (nome_comp,))
            resultado = cursor.fetchone()

            if resultado:
                comp_id = resultado[0]
            else:
                cursor.execute("INSERT INTO competencias (nome) VALUES (?)", (nome_comp,))
                comp_id = cursor.lastrowid
            
            # Liga ao funcionário
            cursor.execute("""
                INSERT OR IGNORE INTO funcionario_competencias 
                (id_funcionario, id_competencia) VALUES (?, ?)
            """, (id_func, comp_id))

        conn.commit()
        flash("Questionário salvo com sucesso!", "sucesso")
        return redirect(url_for('home.home_pag'))
  
    except sqlite3.Error as e:
        print(f"Erro ao salvar: {e}")
        conn.rollback()
        flash("Erro ao salvar o questionário!", "erro")
        
    finally:
        conn.close()

    return redirect('/')