from flask import Blueprint, render_template, session, redirect, url_for

# Blueprint focado apenas na navegação pós-login
bp_home = Blueprint('home', __name__)

@bp_home.route('/home')
def home_pag():
     # Verifica se usuário está logado
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Busca o tipo e nome da sessão
    tipo = session.get('tipo')
    nome = session.get('usuario_nome')
    
    # Renderiza o template correto baseado no tipo
    if tipo == 'funcionario':
        return render_template('home_func.html', nome=nome, tipo=tipo)
    elif tipo == 'empresa':
        return render_template('home_emp.html', nome=nome, tipo=tipo)
    elif tipo == 'google':
        google_user = session.get('user', {})
        return render_template('home_func.html',
                               nome= google_user.get('nome', 'usuário google'),
                               tipo='google',
                               user= google_user)
                               
    else:
        return redirect('/')

@bp_home.route('/logout')
def logout():
    session.clear()
    return redirect('/')