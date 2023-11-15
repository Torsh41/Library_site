import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    REMEMBER_COOKIE_DURATION = timedelta(days=10)
    PERMANENT_SESSION_LIFETIME = REMEMBER_COOKIE_DURATION
    SECRET_KEY = 'I am number one'
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'I am Mister Max'
    JWT_ALGORITHM = 'HS256'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_RECORD_QUERIES = True
    MAX_CONTENT_LENGTH = 1024 * 1024
    #SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JWT_EXPIRATION = 1800
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465#587
    MAIL_USE_SSL = True#False
    MAIL_USE_TLS = False#True
    MAIL_USERNAME = 'leokazantsev19@gmail.com' #(os.environ.get('MAIL_USERNAME'))
    MAIL_PASSWORD = 'qctetuaboxunlvkv' #os.environ.get('MAIL_PASSWORD')
    MBK_MAIL_SUBJECT_PREFIX = '[Magic Book Keeper]' 
    MBK_MAIL_SENDER = 'MBK Admin <MBK@example.com>' 
    MBK_ADMIN = ['leokazantsev19@mail.ru'] #will array from three elements
    
    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
        
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
        
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    "postgresql://rootroot:rootroot@localhost/" + "prod_db.db"
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }