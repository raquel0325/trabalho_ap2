from flask import Flask, url_for, redirect, session, render_template, Blueprint, flash
from authlib.integrations.flask_client import OAuth
import requests
from database import conectar_banco
import json
import secrets
import sqlite3 
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Criamos o Blueprint
bp_google = Blueprint('google_auth', __name__)

# Configurações do google - AGORA VINDO DO .env
appConfig = {
    "OAUTH2_CLIENT_ID": os.getenv('GOOGLE_CLIENT_ID'),
    "OAUTH2_CLIENT_SECRET": os.getenv('GOOGLE_CLIENT_SECRET'),
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key-mude-isso'),
    "FLASK_PORT": "5000"
    }

secret = appConfig.get("FLASK_SECRET")

oauth = OAuth()
def init_oauth(app):
    """Inicializa o OAuth com o app Flask"""
    # Registrar o cliente FIRST
    oauth.register(
        name='google',
        client_id=appConfig["OAUTH2_CLIENT_ID"],
        client_secret=appConfig["OAUTH2_CLIENT_SECRET"],
        server_metadata_url=appConfig["OAUTH2_META_URL"],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    # Depois inicializar com o app
    oauth.init_app(app)



@bp_google.route("/google-login")
def google_login():
    #gera um id
    nonce = secrets.token_urlsafe(16)
    session['google_nonce'] = nonce
    #inicia login com google
    redirect_uri = url_for('google_auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp_google.route('/signin-google')
def google_callback():
    """Callback do Google após login"""
    try:
        # Obtém o token de acesso
        token = oauth.google.authorize_access_token()
        access_token = token.get('access_token')
        
        if not access_token:
            flash("Não foi possível obter token de acesso", "erro")
            return redirect('/')
        
        # Busca informações do usuário via API do Google
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        
        if response.status_code != 200:
            print(f"Erro na API do Google: {response.status_code} - {response.text}")
            flash("Erro ao obter informações do Google", "erro")
            return redirect('/')
        
        user_info = response.json()
        email = user_info.get('email')
        nome = user_info.get('name')
        
        if not email:
            flash("Não foi possível obter seu email do Google", "erro")
            return redirect('/')
        
        print(f"Login Google - Email: {email}, Nome: {nome}")  # Debug
        
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Verifica se o usuário já existe
        cursor.execute("SELECT id_funcionario, telefone, cpf FROM funcionarios WHERE email = ?", 
                       (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Usuário já existe
            session['usuario_id'] = existing_user[0]
            session['usuario_nome'] = nome
            session['tipo'] = 'funcionario'
            
            # Verifica se tem telefone E cpf
            tem_telefone = existing_user[1] is not None and existing_user[1] != ''
            tem_cpf = existing_user[2] is not None and existing_user[2] != ''
            session['dados_incompletos'] = not (tem_telefone and tem_cpf)
            
            conn.close()
            flash(f"Bem-vindo de volta, {nome}!", "sucesso")
            return redirect(url_for('home.home_pag'))
        
        else:
            # Novo usuário - cadastra sem telefone e cpf
            cursor.execute('''
                INSERT INTO funcionarios (nome, email, senha, cpf, telefone)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, email, 'google_oauth', '', ''))
            conn.commit()
            
            novo_id = cursor.lastrowid
            conn.close()
            
            session['usuario_id'] = novo_id
            session['usuario_nome'] = nome
            session['tipo'] = 'funcionario'
            session['dados_incompletos'] = True
            
            flash("Cadastro realizado com sucesso! Complete seus dados no perfil.", "info")
            return redirect(url_for('home.home_pag'))
        
    except Exception as e:
        print(f"Erro detalhado no login Google: {e}")
        import traceback
        traceback.print_exc()
        flash("Erro ao fazer login com Google", "erro")
        return redirect('/')