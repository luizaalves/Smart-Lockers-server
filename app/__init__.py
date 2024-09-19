from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import pymysql
from flask_nav import Nav

# Internal module imports

# MySQL Driver Configuration
pymysql.install_as_MySQLdb()

# Extension instances
nav = Nav()
db = SQLAlchemy()  # SQLAlchemy instance

def create_app(config_class='config.Config'):
    """
    Flask app factory.
    
    Args:
        config_class (str): Configuration class path.

    Returns:
        Flask app: Flask application configured.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    from app.login import login_manager
    login_manager.init_app(app)
    db.init_app(app)
    Bootstrap(app)
    nav.init_app(app)

    # Application context
    with app.app_context():
        from .routes import init_routes
        from .models import compartment, locker, user, locker_schedules,compartment_usage
        from .flask_mqtt import init_mqtt
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        init_routes(app)
        db.create_all()  # Create tables in the database
        app.config['MQTT_BROKER_URL'] = os.getenv("MQTT_BROKER_URL")  # URL do broker MQTT
        app.config['MQTT_BROKER_PORT'] = int(os.getenv("MQTT_BROKER_PORT"))        # Porta do broker MQTT
        app.config['MQTT_USERNAME'] = os.getenv("MQTT_USERNAME")             # Usuário MQTT, se necessário
        app.config['MQTT_PASSWORD'] = os.getenv("MQTT_PASSWORD")             # Senha MQTT, se necessário
        app.config['MQTT_KEEPALIVE'] = int(os.getenv("MQTT_KEEPALIVE"))            # Keep-alive para a conexão MQTT
        app.config['MQTT_TLS_ENABLED'] = False       # TLS, se necessário


        app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")  # Exemplo com o Gmail
        app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")  # Substitua pelo seu e-mail
        app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")  # Substitua pela sua senha de e-mail
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")  # Nome e e-mail do remetente
        
        init_mqtt(app)

    return app
