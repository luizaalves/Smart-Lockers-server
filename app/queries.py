from sqlalchemy import select, delete, update
from flask import current_app
from datetime import datetime
from . import db
from .models.user import User
from .models.compartment_usage import CompartmentUsage
from .models.compartment import Compartment
from .models.locker_schedules import LockerSchedules
from .models.locker import Lockers
from .models.forgot_password import ForgotPassword

def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(int(timestamp))

with current_app.app_context():
    def get_user_by_tag(tag):
        """Retorna um usuário pela tag."""
        statement = select(User).filter_by(tag=tag)
        user = db.session.execute(statement).scalars().first()
        return user
        
    def get_compartment_usage(user):
        """Retorna um compartimento em uso pelo usuário."""
        statement = select(CompartmentUsage).filter_by(user_id=user.id)
        compartment_usage = db.session.execute(statement).scalars().first()
        return compartment_usage
    
    def set_compartment_usage(open_time, close_time, user_id, locker_id, num):
        """Configura um compartimento em uso """
        statement = select(Compartment).filter_by(locker_id=locker_id, number = num)
        compartment = db.session.execute(statement).scalars().first()

        compart_use = CompartmentUsage(
            id_user = user_id,
            id_compartment = compartment.id,
            open_time= timestamp_to_datetime(open_time),
            close_time = timestamp_to_datetime(close_time)
        )

        db.session.add(compart_use)
        db.session.commit()
    
    def set_locker_schedule(open_time, close_time, id_user, locker_id, num):
        """Registra o uso de um compartimento"""
        statement = select(Compartment).filter_by(locker_id=locker_id, number = num)
        compartment = db.session.execute(statement).scalars().first()
        
        statement = select(CompartmentUsage).filter_by(compartment_id=compartment.id)
        compartment_usage_list = db.session.execute(statement).scalars().all()

        for compartment_usage in compartment_usage_list:
            statement = select(User).filter_by(id=compartment_usage.user_id)
            user = db.session.execute(statement).scalars().first()

            stmt = delete(CompartmentUsage).where(CompartmentUsage.user == compartment_usage.user)
            db.session.execute(stmt)
            db.session.commit()

            statement = select(Compartment).filter_by(locker_id=locker_id, number = num)
            compartment = db.session.execute(statement).scalars().first()

            locker_schedule = LockerSchedules(
                id_user = compartment_usage.user.id,
                id_compartment = compartment.id,
                open_time= compartment_usage.open_time,
                close_time = compartment_usage.close_time,
                retrieve_time = timestamp_to_datetime(open_time),
                end_retrieve_time = timestamp_to_datetime(close_time)
            )

            db.session.add(locker_schedule)
            db.session.commit()
        
    def get_locker(locker_name):
        """Retorna o locker pelo nome"""
        statement = select(Lockers).filter_by(name=locker_name)
        locker = db.session.execute(statement).scalars().first()
        return locker
        
    def check_compartment_by_num(num, locker_id):
        """Retorna o objeto compartimento a partir do nome e locker id"""
        statement = select(Compartment).filter_by(number=num)
        compartment = db.session.execute(statement).scalars().first()
        if compartment is not None:
            if compartment.locker_id == locker_id:
                return compartment
        return None

    def get_compartment_by_id(id):
        """Retorna o objeto compartimento a partir do id"""
        statement = select(Compartment).filter_by(id=id)
        compartment = db.session.execute(statement).scalars().first()
        return compartment
    
    def set_locker(locker_name):
        """Configura um compartimento a partir do nome do armário"""
        locker = Lockers (
            name= locker_name
        )
        db.session.add(locker)
        db.session.commit()

    def set_compartment(locker_id, num):
        """Configura um compartimento a partir do número e locker id"""
        statement = select(Compartment).filter_by(locker_id=locker_id, number=num)
        existing_compartment = db.session.execute(statement).scalars().first()
        if existing_compartment:
            print("A combinação locker_id e number já existe.")
            return
        try:
            compartment_obj = Compartment (
                locker_id = locker_id,
                number = num
            )
            db.session.add(compartment_obj)
            db.session.commit()
        except ValueError:
            return
    
    def get_admins():
        """Retorna uma lista com todos os e-mails dos administradores do sistema"""
        users_admins = db.session.query(User.email).filter(User.user_type == "admin").all()

        return [email[0] for email in users_admins]
    
    def get_available_compartments(locker_id):
        """Retorna compartimentos disponiveis pelo locker id"""
        used_compartments_subquery = (
            db.session.query(CompartmentUsage.compartment_id)
            .join(Compartment, Compartment.id == CompartmentUsage.compartment_id)
            .filter(Compartment.locker_id == locker_id)
            .subquery()
        )

        available_compartments = (
            db.session.query(Compartment.number)
            .filter(
                Compartment.locker_id == locker_id,
                Compartment.id.notin_(used_compartments_subquery)
            )
            .all()
        )

        available_compartments_numbers = [compartment.number for compartment in available_compartments]
        
        return available_compartments_numbers
    
    def set_code_validation_password(email, code, time_generated):
        """Configura o código de validação para o 'Esqueceu sua senha'; com 15 minutos de validade"""
        statement = select(User).filter_by(email=email)
        user = db.session.execute(statement).scalars().first()
        if user is not None:
            statement = select(ForgotPassword).filter_by(user=user)
            forgot_password = db.session.execute(statement).scalars().first()
            if forgot_password is None:
                password = ForgotPassword (
                    code_generated= code,
                    id_user=user.id,
                    date_time = time_generated
                )
                db.session.add(password)
                db.session.commit()
            else:
                stmt = (
                    update(ForgotPassword).
                    where(ForgotPassword.user_id == user.id).
                    values(code=code, date_time=time_generated)
                )
                db.session.execute(stmt)
                db.session.commit()

    def get_date_from_code_validation_password(code):
        """Retorna a data gerada do código para validação no 'esqueceu sua senha'"""
        statement = select(ForgotPassword).filter_by(code=code)
        forgot_password = db.session.execute(statement).scalars().first()

        if forgot_password is not None:
            return forgot_password.date_time
        return None
    
    def get_email_from_code_validation_password(code):
        """Retorna o e-mail a partir do código para validação no 'esqueceu sua senha'"""
        statement = select(ForgotPassword).filter_by(code=code)
        forgot_password = db.session.execute(statement).scalars().first()

        if forgot_password is not None:
            return forgot_password.user.email
        return None
    
    def update_password_user(email, new_password):
        "Atualiza a senha do usuário a partir do e-mail"
        statement = select(User).filter_by(email=email)
        user = db.session.execute(statement).scalars().first()
        if user is not None:
            user.password = user.set_password(new_password)
            db.session.commit()

    def get_compartment_by_compartment_in_use_user(user_id):
        """Retorna o objeto compartimento a partir do id do usuario caso esteja associado a algum compartimento em uso"""
        statement = select(CompartmentUsage).filter_by(user_id=user_id)
        compartment_in_use = db.session.execute(statement).scalars().first()
        statement = select(Compartment).filter_by(id=compartment_in_use.compartment_id)
        compartment = db.session.execute(statement).scalars().first()
        return compartment
    
    def get_user_by_id(id_user):
        """Retorna o objeto usuário a partir do seu id"""
        statement = select(User).filter_by(id=id_user)
        usuario = db.session.execute(statement).scalars().first()
        return usuario
    
    def get_user_by_email(email):
        statement = select(User).filter_by(email=email)
        usuario = db.session.execute(statement).scalars().first()
        return usuario
    
    def set_user(nome, email, senha, tag, user_type):
        usuario = User(
            name= nome,
            email=email,
            password=senha,
            tag=tag,
            user_type=user_type
        )
        db.session.add(usuario)
        db.session.commit()
    
    def set_password_admin_user(usuario):
        try:
            if(usuario.password == 'admin'):
                usuario.set_password('admin')
                db.session.commit()
        except:
            pass

    def update_email_user(old_email, new_email, password):
        statement = select(User).filter_by(email=old_email)
        user = db.session.execute(statement).scalars().first()
        user.email = new_email
        if(user.check_password(password)):
            db.session.commit()

    def update_admin_user(email, name, tag, password):
        statement = select(User).filter_by(email='admin')
        user = db.session.execute(statement).scalars().first()
        user.email = email
        user.name = name
        user.tag = tag
        user.password = password
        db.session.commit()

    def get_compartment_by_compartiment_in_use_by_user(user_id):
        statement = select(CompartmentUsage).filter_by(user_id=user_id)
        compartment_in_use = db.session.execute(statement).scalars().first()
        if compartment_in_use is not None:
            statement = select(Compartment).filter_by(id=compartment_in_use.compartment_id)
            compartment = db.session.execute(statement).scalars().first()
            return compartment
        return None
    
    def get_compartment_by_number(num, locker_id):
        statement = select(Compartment).filter_by(number=num, locker_id=locker_id)
        compartment = db.session.execute(statement).scalars().first()
        return compartment
    
    def get_compartment_in_use_by_id_comp(id_compartment):
        statement = select(CompartmentUsage).filter_by(compartment_id=id_compartment)
        compartment_in_use = db.session.execute(statement).scalars().first()
        return compartment_in_use
    
    def set_compartment_in_use_now(user_id, compartment_id, open_time, close_time):
        new_compartment_in_use = CompartmentUsage(
            id_user=user_id,
            open_time=open_time,
            close_time=close_time,
            id_compartment=compartment_id
        )
        db.session.add(new_compartment_in_use)
        db.session.commit()

    def get_all_lockers():
        return LockerSchedules.query.all()
    
    def get_all_compartiment_in_use():
        return CompartmentUsage.query.all()
    
    def get_all_lockers_schedules_by_id_user(user_id):
        statement = select(LockerSchedules).filter_by(user_id=user_id)
        locker_schedules = db.session.execute(statement).scalars().all()
        return locker_schedules
    
    def get_all_compartment_in_use_by_id_user(user_id):
        statement = select(CompartmentUsage).filter_by(user_id=user_id)
        compartment_in_use = db.session.execute(statement).scalars().all()
        return compartment_in_use
