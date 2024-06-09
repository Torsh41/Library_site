from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from config import config


app = Flask(__name__, template_folder='templates')
socketio = SocketIO(async_mode='eventlet')
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()
moment = Moment()
database = SQLAlchemy()
migrate = Migrate(app, database)  
#manager = Manager(app)


def create_app(config_name):
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)
  socketio.init_app(app)
  mail.init_app(app)
  moment.init_app(app)
  login_manager.init_app(app)
  
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/auth')
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)
  from .personal import personal as personal_blueprint
  app.register_blueprint(personal_blueprint, url_prefix='/user')
  from .admin import admin as admin_blueprint
  app.register_blueprint(admin_blueprint, url_prefix='/admin')
  
  database.init_app(app)
  with app.app_context():
    database.create_all()
    # database.drop_all()
      
  # здесь выполняется подключение маршрутов и
  # нестандартных страниц с сообщениями об ошибках
  return app
