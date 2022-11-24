from email.policy import default
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .init import database, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime

#отношение один ко многим, User->Cataloge - один к одному

class User(UserMixin, database.Model):
    __tablename__ = "users"
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(64), unique=True, index=True)
    username = database.Column(database.String(64), unique=True)
    city = database.Column(database.Text, default=False)
    gender = database.Column(database.Boolean, default=False)
    age = database.Column(database.Integer, default=False)
    about_me = database.Column(database.Text, default=False)
    password_hash = database.Column(database.String(128))
    books = database.relationship('Book', backref='user')
    grades = database.relationship('BookGrade', backref='user')
    comments = database.relationship('Comment', backref='user')
    cataloge = database.relationship('Cataloge', backref='user', uselist=False)
    confirmed = database.Column(database.Boolean, default=False)
    is_admin = database.Column(database.Boolean, default=False)
    
    def generate_confirmation_token(self, expiration=36000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        database.session.add(self)
        return True
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def check_admin(self):
        if current_app.config['FLASKY_ADMIN'] == self.email:
            self.is_admin = True
     
         
class Book(database.Model):
    __tablename__ = "books"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), unique=True)
    author = database.Column(database.String(64), unique=False)
    description = database.Column(database.Text(), unique=True)
    date = database.Column(database.Date(), unique=False)
    count_of_chapters = database.Column(database.Integer, unique=False)
    genre = database.Column(database.String(64), unique=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    

class BookGrade(database.Model):
    __tablename__ = "grades"
    id = database.Column(database.Integer, primary_key=True)
    bookname = database.Column(database.String(64))
    grade = database.Column(database.Integer)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id')) 


class Comment(database.Model):
    __tablename__ = "comments"
    id = database.Column(database.Integer, primary_key=True)
    body = database.Column(database.Text)
 #body_html = database.Column(database.Text)
    timestamp = database.Column(database.DateTime, index=True, default=datetime.utcnow)
 #disabled = database.Column(database.Boolean)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
 #post_id = database.Column(db.Integer, db.ForeignKey('posts.id'))


#lists and items models
class Cataloge(database.Model):
    __tablename__ = "catalogues"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), unique=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    items = database.relationship('Item', backref='cataloge', cascade = "all, delete, delete-orphan")


class Item(database.Model):
    __tablename__ = "items"
    id = database.Column(database.Integer, primary_key=True)
    read = database.Column(database.String(64), unique=False, default=None) #прочитано 
    read_in_process = database.Column(database.String(64), unique=False, default=None) #читаю
    planning = database.Column(database.String(64), unique=False, default=None) #планирую
    abandoned = database.Column(database.String(64), unique=False, default=None) #заброшено 
    cataloge_id = database.Column(database.Integer, database.ForeignKey('catalogues.id')) 
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    