from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from flask_migrate import Migrate


application = Flask(__name__, template_folder='templates')
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()
moment = Moment()
database = SQLAlchemy()
migrate = Migrate(application, database)