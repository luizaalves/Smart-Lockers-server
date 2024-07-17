import flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, session, jsonify, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_nav.elements import Navbar, View, Text
import logging
from sqlalchemy.orm import Session
from sqlalchemy import select

# Internal module imports
from . import nav,db
from .forms import *
from .models.user import User

@nav.navigation()
def menu():
    """
    Cria o menu de navegação para o Smart Locks Server.

    Esta função define a barra de navegação usando a biblioteca Flask-Nav.
    O menu muda dinamicamente com base no estado de login do usuário e seu
    tipo (admin ou comum).

    Se o usuário estiver logado:
        - Exibe uma mensagem de saudação com o nome do usuário.
        - Adiciona opções de menu específicas para administradores, como 
          'Registrar usuário' e 'Atualizar e-mail/senha do usuário'.
        - Adiciona a opção 'Exit' para permitir que o usuário saia.

    Se o usuário não estiver logado:
        - Exibe apenas a opção de menu 'Início'.

    Returns:
        Navbar: O objeto Navbar configurado com os itens de menu apropriados.
    """
    menu = Navbar('Smart Locks Server')
    if session.get('logado'):
        user_id = session['usuario']
        statement = select(User).filter_by(id_user=user_id)
        usuario_logado = db.session.execute(statement).scalars().first()
        menu.items.append(Text('Hello, '+usuario_logado.name))
        if(usuario_logado.user_type=='admin'):
            menu.items.append(View('Registrar usuário', 'register'))
            if(usuario_logado.email!='admin'):
                menu.items.append(View('Atualizar e-mail usuário', 'update_email'))
                menu.items.append(View('Atualizar senha usuário', 'update_password'))
        menu.items.append(View('Exit', 'sair'))
        return menu
    menu.items = [View('Início', 'inicial')]
    return menu
    
def init_routes(app):
    @app.route('/')
    def inicial():
        """
        Renderiza a página de navegação para o Smart Locks Server.

        Esta função define a página de navegação da rota principal usando a biblioteca Flask-session.
        A página muda dinamicamente com base no estado de usuário logado ou não.
        
        Se o usuário estiver logado:
            - Renderiza a página 'index.html', exibindo informações perminentes ao usuário logado.
            - O menu exibido muda dinamicante de acordo com o tipo de usuário.

        Se o usuário não estiver logado:
            - Renderiza a página 'login.html'.

        Returns:
            Redirect: O redirecionamento para a página.
        """
        if session.get('logado'):
            return render_template('index.html')
        session['usuario'] = None
        session['logado'] = False
        return flask.redirect(flask.url_for('login'))
    
    @app.route('/sair')
    @login_required
    def sair():
        logout_user()
        session['logado'] = False
        session['usuario'] = None
        logging.info('Você foi desconectado com sucesso.', 'success')
        return redirect(url_for('login'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            statement = select(User).filter_by(email=form.email.data)
            usuario = db.session.execute(statement).scalars().first()
            if(usuario.password == 'admin'):
                usuario.set_password('admin')
                db.session.commit()
            if usuario is not None:
                if usuario.check_password(form.password.data):
                    session['logado']=True
                    session['usuario']=usuario.id_user
                    print(f'Usuário logado com ID: {session["usuario"]}, nome: {usuario.name}')
                    login_user(usuario)
                    if(usuario.email=='admin'):
                        return flask.redirect(flask.url_for('update'))
                    return flask.redirect(flask.url_for('inicial'))
                else:
                    return render_template('login.html', form=form)
        session['usuario'] = None
        session['logado'] = False
        return render_template('login.html', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if request.method == 'POST':
            logging.info('Form submitted')
            if form.validate_on_submit():
                usuario = User(
                    name= form.nome.data,
                    email=form.email.data,
                    password=form.senha.data,
                    tag=form.tag.data,
                    user_type=form.tipo_usuario.data
                )
                db.session.add(usuario)
                db.session.commit()
                logging.info('User registered successfully')
                return redirect(url_for('inicial'))
            else:
                logging.error('Form validation failed')
                logging.error(form.errors)
                return render_template('register.html', form=form)
        return render_template('register.html', form=form)

    @app.route('/check_email', methods=['POST'])
    def check_email():
        email = request.form.get('email')
        statement = select(User).filter_by(email=email)
        user = db.session.execute(statement).scalars().first()
        if user:
            return jsonify({'exists': True})
        return jsonify({'exists': False})
    
    @app.route('/update-email', methods=['GET', 'POST'])
    @login_required
    def update_email():
        form = UpdateEmailForm()
        if form.validate_on_submit():
            statement = select(User).filter_by(email=form.old_email.data)
            user = db.session.execute(statement).scalars().first()
            user.email = form.email.data
            user.name = form.nome.data
            user.user_type=form.tipo_usuario.data
            if(user.check_password(form.senha.data)):
                db.session.commit()
                print('Suas informações foram atualizadas com sucesso!')
                return redirect(url_for('inicial'))
        return render_template('update_email.html', form=form)
    
    @app.route('/update-password', methods=['GET', 'POST'])
    @login_required
    def update_password():
        form = UpdatePasswordForm()
        if form.validate_on_submit():
            statement = select(User).filter_by(email=form.email.data)
            user = db.session.execute(statement).scalars().first()
            user.email = form.email.data
            user.name = form.nome.data
            user.user_type=form.tipo_usuario.data
            user.password = user.set_password(form.confirmar_senha.data)
            db.session.commit()
            print('Suas informações foram atualizadas com sucesso!')
            return redirect(url_for('inicial'))
        return render_template('update_password.html', form=form)
    
    @app.route('/update', methods=['GET', 'POST'])
    @login_required
    def update():
        if current_user.email != 'admin':
            print('Acesso negado: você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('inicial'))
        form = UpdateEmailPasswordForm()
        if form.validate_on_submit():
            statement = select(User).filter_by(email='admin')
            user = db.session.execute(statement).scalars().first()
            user.email = form.email.data
            user.name = form.nome.data
            user.tag = form.tag.data
            user.password = form.confirmar_senha.data
            db.session.commit()
            print('Suas informações foram atualizadas com sucesso!')
            return redirect(url_for('inicial'))
        return render_template('update.html', form=form)
    