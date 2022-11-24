from flask_bootstrap import Bootstrap4
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap4()
mail = Mail()
moment = Moment()
database = SQLAlchemy()
