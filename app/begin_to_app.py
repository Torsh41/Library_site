from app.init import *
from config import config
from .auth import auth as auth_blueprint
from .main import main as main_blueprint
from .personal import personal as personal_blueprint


def create_app(config_name):
  application.config.from_object(config[config_name])
  config[config_name].init_app(application)
  mail.init_app(application)
  moment.init_app(application)
  login_manager.init_app(application)
  application.register_blueprint(auth_blueprint, url_prefix='/auth')
  application.register_blueprint(main_blueprint)
  application.register_blueprint(personal_blueprint, url_prefix='/user')
  database.init_app(application)
  with application.app_context():
    database.create_all()
    
  # здесь выполняется подключение маршрутов и
  # нестандартных страниц с сообщениями об ошибках
  return application
