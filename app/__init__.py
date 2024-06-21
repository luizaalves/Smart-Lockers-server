from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import pymysql
from flask_nav import Nav
import threading

# Internal module imports
from .models import User  # Models module from db import
from .mqtt import mqtt_client

# MySQL Driver Configuration
pymysql.install_as_MySQLdb()

# Extension instances
login_manager = LoginManager()
nav = Nav()
db = SQLAlchemy()  # SQLAlchemy instance

@login_manager.user_loader
def load_user(user_id):
    """
    Callback used by Flask-Login to load a user.
    """
    return User.user_load(user_id)

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
    login_manager.init_app(app)
    db.init_app(app)
    Bootstrap(app)
    nav.init_app(app)

    # Application context
    with app.app_context():
        from .routes import init_routes
        init_routes(app)
        db.create_all()  # Create tables in the database

    # Initialize the MQTT client in a separate thread
    mqtt_thread = threading.Thread(target=mqtt_client.init_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    return app
