import flask, logging, random, string, pytz
from flask import render_template, session, jsonify, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_nav.elements import Navbar, View, Text
from sqlalchemy import select
from datetime import datetime, timedelta
from .queries import *
from flask_mail import Mail, Message

from . import nav,db
from .forms import *
from .models.user import User
from .models.locker import Lockers
from .models.locker_schedules import LockerSchedules
from .models.compartment_usage import CompartmentUsage
from .models.compartment import Compartment

def init_routes(app):

    @app.route('/edit_number', methods=['GET', 'POST'])
    def edit_number():
        if session.get('logado'):
            user_id = session['usuario']
            statement = select(User).filter_by(id=user_id)
            usuario = db.session.execute(statement).scalars().first()
            if(usuario.user_type=='admin'):
                statement = select(CompartmentUsage).filter_by(user_id=user_id)
                compartment_in_use = db.session.execute(statement).scalars().first()
                statement = select(Compartment).filter_by(id=compartment_in_use.compartment_id)
                compartment = db.session.execute(statement).scalars().first()

                form = CompartmentAdmin()

                if form.validate_on_submit():
                    novo_valor = form.compartment.data

                if compartment:
                    form.compartment.data = compartment.number
                return render_template('locker_schedule.html', form=form)

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
            statement = select(User).filter_by(id=user_id)
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

    @app.route('/', methods=['GET', 'POST'])
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
            form = CompartmentAdmin()
            user_id = session['usuario']
            statement = select(User).filter_by(id=user_id)
            usuario = db.session.execute(statement).scalars().first()
            locker_schedules = None
            if(usuario.user_type == 'admin'):
                statement = select(CompartmentUsage).filter_by(user_id=user_id)
                compartment_in_use = db.session.execute(statement).scalars().first()
                
                if compartment_in_use is not None:
                    statement = select(Compartment).filter_by(id=compartment_in_use.compartment_id)
                    compartment = db.session.execute(statement).scalars().first()
                    print(f"compartment num: {compartment.number}")

                    if compartment is not None:
                        form.compartment.data = compartment.number
                        form.locker_name.data = compartment.locker.name

                if form.validate_on_submit():
                    statement = select(Lockers).filter_by(name=form.locker_name.data)
                    locker = db.session.execute(statement).scalars().first()
                    if locker is not None:
                        statement = select(Compartment).filter_by(number=form.compartment.data, locker_id=locker.id)#add o locker_name
                        compartment = db.session.execute(statement).scalars().first()
                        if compartment is not None:
                            statement = select(CompartmentUsage).filter_by(compartment_id=compartment.id)
                            compartment_in_use = db.session.execute(statement).scalars().first()
                            if compartment_in_use is not None:
                                new_compartment_in_use = CompartmentUsage(
                                    id_user=user_id,
                                    open_time=datetime.now(),
                                    close_time=datetime.now(),
                                    id_compartment=compartment.id
                                )
                                db.session.add(new_compartment_in_use)
                                db.session.commit()
                                return redirect(url_for('inicial'))

                locker_schedules = LockerSchedules.query.all()    
                compartment_in_use = CompartmentUsage.query.all()
            else:
                statement = select(LockerSchedules).filter_by(user_id=user_id)
                locker_schedules = db.session.execute(statement).scalars().all()
                statement = select(CompartmentUsage).filter_by(user_id=user_id)
                compartment_in_use = db.session.execute(statement).scalars().first()

            return render_template('locker_schedule.html', locker_schedules=locker_schedules, compartment_in_use=compartment_in_use, type = usuario.user_type, form=form)
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
            try:
                if(usuario.password == 'admin'):
                    usuario.set_password('admin')
                    db.session.commit()
            except:
                pass
            if usuario is not None:
                if usuario.check_password(form.password.data):
                    session['logado']=True
                    session['usuario']=usuario.id
                    print(f'Usuário logado com ID: {session["usuario"]}, nome: {usuario.name}')
                    login_user(usuario)
                    if(usuario.email=='admin'):
                        return flask.redirect(flask.url_for('update'))
                    return flask.redirect(flask.url_for('inicial'))
                else:
                    return render_template('login.html', form=form)
        elif form.forgot_password.data:
            return redirect(url_for('forgot_password'))
        session['usuario'] = None
        session['logado'] = False
        return render_template('login.html', form=form)
    
    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        form = ForgotPasswordForm()
        timezone = pytz.timezone("America/Sao_Paulo")
        if form.validate_on_submit():
            if form.submit.data:
                email = form.email.data
                date_time = datetime.now(timezone)
                code=random_string(6)
                set_code_validation_password(code=code, email=email, time_generated=date_time)
                mail = Mail(app)
                msg = Message(
                    'Smart Lockers - Reset Password',  sender='smart.lockers.notification@gmail.com',
                    recipients = str(email).split()
                )
                msg.body = f"Code to reset password {code}. \nValid for 15 minutes."
                
                mail.send(msg)

            elif form.submit_code.data:  
                any_date = get_date_from_code_validation_password(form.code.data)

                if any_date is not None and any_date.tzinfo is None:
                    any_date = timezone.localize(any_date)

                date_time = datetime.now(timezone)
                if date_time - any_date < timedelta(minutes=15):
                    return redirect(url_for('reset_password', email=get_email_from_code_validation_password(form.code.data)))
                else:
                    return redirect(url_for('login'))
        return render_template('forgot_password.html', form=form)
    @app.route('/reset_password', methods=['GET','POST'])
    def reset_password():
        form = ResetPasswordForm()
        email = request.args.get('email') or session.get('email')
        if request.args.get('email') is not None:
            session['email'] = request.args.get('email')
        form.email.data = email
        if form.validate_on_submit():
            form.new_password.data
            update_password_user(email, form.new_password.data)
            session['email'] = None
            return redirect(url_for('login'))
        return render_template('reset_password.html', form=form, email=email)

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
            update_password_user(form.email.data, form.confirmar_senha.data)
            
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
    
    def random_string(length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    