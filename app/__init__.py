from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import pymysql
from flask_nav import Nav
import threading

# Internal module imports
from .mqtt_client import *

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
        init_routes(app)
        db.create_all()  # Create tables in the database
        # Initialize the MQTT client in a separate thread
        mqtt_thread = threading.Thread(target=mqtt_client.init_mqtt)
        mqtt_thread.daemon = True
        mqtt_thread.start()
    return app
