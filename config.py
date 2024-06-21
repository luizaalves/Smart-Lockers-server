class Config:
    DEBUG = True
    SECRET_KEY = 'string with random text'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user_lockers:password_lockers@localhost/lockers'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
