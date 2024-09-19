class Config:
    from dotenv import load_dotenv
    import os
    load_dotenv()

    DEBUG = True
    SECRET_KEY = 'string with random text'
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
