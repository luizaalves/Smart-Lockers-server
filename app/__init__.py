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
        init_routes(app)
        db.create_all()  # Create tables in the database
        app.config['MQTT_BROKER_URL'] = '192.168.1.7'  # URL do broker MQTT
        app.config['MQTT_BROKER_PORT'] = 1883        # Porta do broker MQTT
        app.config['MQTT_USERNAME'] = ''             # Usuário MQTT, se necessário
        app.config['MQTT_PASSWORD'] = ''             # Senha MQTT, se necessário
        app.config['MQTT_KEEPALIVE'] = 60            # Keep-alive para a conexão MQTT
        app.config['MQTT_TLS_ENABLED'] = False       # TLS, se necessário
        init_mqtt(app)
    return app
