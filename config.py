import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_RECORD_QUERIES = True
    MAX_CONTENT_LENGTH = 1024 * 1024
    #SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    '''
    MAIL_HOSTNAME = 'localhost'
    #MAIL_SERVER = 'smtp.mail.ru'#os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = 25#465#int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = False#os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        #['true', 'on', '1']
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    SSL_REDIRECT = False
    MAIL_USERNAME = None#os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = None#os.environ.get('MAIL_PASSWORD')#'Pistol_packin_never_slackin'
    '''
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465#587
    MAIL_USE_SSL = True#False
    MAIL_USE_TLS = False#True
    MAIL_USERNAME = 'leokazantsev19@gmail.com' #(os.environ.get('MAIL_USERNAME'))
    MAIL_PASSWORD = 'qctetuaboxunlvkv' #os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Magic Book Keeper]' 
    FLASKY_MAIL_SENDER = 'MBK Admin <MBK@example.com>' #<flasky@example.com>
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') #will array from three elements
    
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
    'sqlite:///' + os.path.join(basedir, 'database.sqlite')
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }