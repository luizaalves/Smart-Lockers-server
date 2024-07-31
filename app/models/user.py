from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  UserMixin
from .. import db
from flask import session

NAME_MAX_SIZE = 40
PASS_MAX_SIZE = 40


class User(UserMixin, db.Model):
    """
    Modelo de usuário para o sistema de autenticação.

    Este modelo representa um usuário no banco de dados e inclui métodos
    para manipular dados do usuário, como configuração de senha, verificação
    de senha e recuperação de dados.

    Atributos:
        id_user (int): ID único do usuário, chave primária.
        name (str): Nome do usuário, não pode ser nulo.
        email (str): Endereço de email do usuário, único e não pode ser nulo.
        password (str): Senha do usuário, armazenada como um hash, não pode ser nula.
        user_type (str): Tipo de usuário, por exemplo, admin ou comum, não pode ser nulo.

    Métodos:
        __init__(self, name, email, password, user_type):
            Inicializa um novo objeto User com nome, email, senha e tipo de usuário.

        set_password(self, password):
            Define a senha do usuário, armazenando-a como um hash.

        set_email(self, email):
            Define o endereço de email do usuário.

        check_password(self, password):
            Verifica se a senha fornecida corresponde ao hash armazenado.

        is_active(self):
            Retorna True indicando que a conta do usuário está ativa.

        user_load(user_id):
            Carrega um usuário a partir do banco de dados usando seu ID.

        get_id(self):
            Retorna o ID do usuário como uma string.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String,nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    user_type = Column(String(10), nullable=False)
    tag = Column(String(20))

    compartment_usage = relationship("CompartmentUsage", back_populates='user', lazy=True)
    locker_schedules = relationship("LockerSchedules", back_populates='user', lazy=True)


    def __init__(self, name, email, password, user_type, tag):
        """
        Inicializa um novo objeto User com nome, email, senha e tipo de usuário.

        Args:
            name (str): Nome do usuário.
            email (str): Endereço de email do usuário.
            password (str): Senha do usuário.
            user_type (str): Tipo de usuário (por exemplo, 'admin', 'regular').
        """
        self.name = name
        self.email = email
        self.password = generate_password_hash(password) # TODO Verify why it's not working
        # self.password = password
        self.user_type = user_type
        self.tag = tag
    def set_password(self, password):
        """
        Define a senha do usuário, armazenando-a como um hash.

        Args:
            password (str): A senha do usuário.

        Returns:
            str: A senha armazenada como um hash.
        """
        self.password = generate_password_hash(password) # TODO Verify why it's not working
        return self.password
    
    def set_email(self, email):
        """
        Define o endereço de email do usuário.

        Args:
            email (str): O novo endereço de email do usuário.
        """
        self.email = email

    def check_password(self, password):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.

        Args:
            password (str): A senha a ser verificada.

        Returns:
            bool: True se a senha corresponder, False caso contrário.
        """
        return check_password_hash(self.password, password)
    
    def is_active(self):
        """
        Indica se a conta do usuário está ativa.

        Returns:
            bool: Sempre retorna True.
        """
        return True
    
    def user_load(user_id):
        """
        Carrega um usuário a partir do banco de dados usando seu ID.

        Args:
            user_id (int): O ID do usuário.

        Returns:
            User: O objeto User correspondente ao ID fornecido.
        """
        return session.get(User, user_id)

    def get_id(self):
        """
        Retorna o ID do usuário como uma string.

        Returns:
            str: O ID do usuário.
        """
        return str(self.id)