from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .init import database, login_manager, application
from flask import current_app, url_for
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy_serializer import SerializerMixin


class Role:
    USER = 0
    ADMIN = 1
    

#отношение один ко многим
class User(UserMixin, database.Model, SerializerMixin):
    __tablename__ = "users"
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(64), unique=True, index=True)
    username = database.Column(database.String(64), unique=True, index=True)
    avatar = database.Column(database.LargeBinary, default=False)
    city = database.Column(database.String(64), default=False)
    gender = database.Column(database.String(4), default=False)
    age = database.Column(database.Integer, default=False)
    about_me = database.Column(database.Text, default=False)
    password_hash = database.Column(database.String(128))
    books = database.relationship('Book', backref='user')
    grades = database.relationship('BookGrade', backref='user', cascade="all, delete, delete-orphan")
    comments = database.relationship('Comment', backref='user', cascade="all, delete, delete-orphan")
    cataloges = database.relationship('Cataloge', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")#, uselist=False)
    confirmed = database.Column(database.Boolean, default=False)
    role = database.Column(database.Boolean, default=False)
    
    def generate_confirmation_token(self): #30 минут время действия токена
        now = datetime.utcnow()
        payload = {
            'iat': 0,
            'ref': 0,
            'exp': now + timedelta(seconds=current_app.config['JWT_EXPIRATION']),
            'scope': 'access_token',
            'user': self.username,
        }
        access_token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
        return access_token
    
    def confirm(self, token):
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=current_app.config['JWT_ALGORITHM'])
        except:
            return False
            
        user_data = payload.get('user')
        if user_data != self.username:
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
        try:
            if self.email in current_app.config['MBK_ADMIN']:
                self.role = True
            else:
                self.role = False
        except:
            self.role = False
            
    def default_ava(self):
        with application.open_resource(application.root_path + url_for('static', filename='styles/img/default_avatar.jpg'), 'rb') as f:
            self.avatar = f.read()
            
            
class Category(database.Model, SerializerMixin):
    __tablename__ = "categories"    
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), unique=True, index=True)
    books = database.relationship('Book', backref='category', cascade="all, delete, delete-orphan")
    
    
class Book(database.Model, SerializerMixin):
    __tablename__ = "books"
    id = database.Column(database.Integer, primary_key=True)
    cover = database.Column(database.LargeBinary, default=False)
    isbn = database.Column(database.String(64), unique=False)
    name = database.Column(database.String(64), unique=True, index=True)
    author = database.Column(database.String(64), unique=False)
    publishing_house = database.Column(database.String(64), unique=False)
    description = database.Column(database.Text(), unique=False)
    release_date = database.Column(database.Date(), unique=False)
    count_of_chapters = database.Column(database.Integer, unique=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    category_id = database.Column(database.Integer, database.ForeignKey('categories.id'))
    cataloge_items = database.relationship('Item', backref='book', cascade="all, delete, delete-orphan")
    grades = database.relationship('BookGrade', backref='book', cascade="all, delete, delete-orphan")
    comments = database.relationship('Comment', backref='book', lazy='dynamic', cascade="all, delete, delete-orphan")
    
    def default_cover(self):
        with application.open_resource(application.root_path + url_for('static', filename='styles/img/book.jpg'), 'rb') as f:
            self.cover = f.read()
    

class BookGrade(database.Model, SerializerMixin):
    __tablename__ = "grades"
    id = database.Column(database.Integer, primary_key=True)
    grade = database.Column(database.Integer)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id')) 
    book_id = database.Column(database.Integer, database.ForeignKey('books.id'))


class Comment(database.Model, SerializerMixin):
    __tablename__ = "comments"
    id = database.Column(database.Integer, primary_key=True)
    body = database.Column(database.Text)
    timestamp = database.Column(database.DateTime, index=True, default=datetime.utcnow)
    #disabled = database.Column(database.Boolean)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    book_id = database.Column(database.Integer, database.ForeignKey('books.id'))


#lists and items models
class Cataloge(database.Model, SerializerMixin):
    __tablename__ = "catalogues"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), unique=False, index=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    items = database.relationship('Item', backref='cataloge', cascade="all, delete, delete-orphan")


class Item(database.Model, SerializerMixin):
    __tablename__ = "items"
    id = database.Column(database.Integer, primary_key=True)
    read_state = database.Column(database.String(64), unique=False, default=None) #прочитано или читаю или планирую или заброшено  
    cataloge_id = database.Column(database.Integer, database.ForeignKey('catalogues.id')) 
    book_id = database.Column(database.Integer, database.ForeignKey('books.id')) 


class SearchResult(database.Model, SerializerMixin):
    __tablename__ = "search_results"
    id = database.Column(database.Integer, primary_key=True)
    cover = database.Column(database.LargeBinary, default=False)
    isbn = database.Column(database.String(64), unique=False)
    name = database.Column(database.String(64), unique=True, index=True)
    author = database.Column(database.String(64), unique=False)
    publishing_house = database.Column(database.String(64), unique=False)
    description = database.Column(database.Text(), unique=False)
    release_date = database.Column(database.Date(), unique=False)
    count_of_chapters = database.Column(database.Integer, unique=False)
    def __init__(self, book):
        self.id = book.id
        self.cover = book.cover
        self.isbn = book.isbn
        self.name = book.name
        self.author = book.author
        self.publishing_house = book.publishing_house
        self.description = book.description
        self.release_date = book.release_date
        self.count_of_chapters = book.count_of_chapters
    
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    