import os, json
from datetime import timedelta
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class Config:
    REMEMBER_COOKIE_DURATION = timedelta(days=10)
    PERMANENT_SESSION_LIFETIME = REMEMBER_COOKIE_DURATION
    SECRET_KEY = 'I am number one'
    JWT_SECRET_KEY = os.getenv('SECRET_KEY') or 'I am Mister Max'
    JWT_ALGORITHM = 'HS256'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 1024 * 1024
    JWT_EXPIRATION = 1800
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', default="")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', default="")
    MBK_MAIL_SUBJECT_PREFIX = os.getenv('MBK_MAIL_SUBJECT_PREFIX', default="[Magic Book Keeper]")
    MBK_MAIL_SENDER = os.getenv('MBK_MAIL_SENDER', default="The MBK team <MBK@example.com>")
    MBK_ADMIN = json.loads(os.getenv('MBK_ADMIN', default="[]"))

    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
        
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
        
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
    "postgresql://" + os.getenv("POSTGRES_USER") + ":" + os.getenv("POSTGRES_PASSWORD") + "@lib-db" + "/" + os.getenv("POSTGRES_DB")
    #NOTE: `lib-db` is the docker container name AND ip address
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }
