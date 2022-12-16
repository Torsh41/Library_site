from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange
from wtforms import ValidationError
from ..models import Book, Cataloge, User
from flask_login import current_user


class EditProfileForm(FlaskForm):
    avatar = FileField('Photo')
    city = StringField('City', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название города должно содержать только буквы и пробелы.')])
    age = IntegerField('Age', validators=[DataRequired('Поля не должны быть пустыми.'), NumberRange(1, 100, message='Здесь невозможно ошибиться:)')])
    description = TextAreaField('Description', validators=[DataRequired('Поля не должны быть пустыми.')])
    submit = SubmitField('Сохранить')
    
    
def validate_list_name(form, field): 
    catalogues = Cataloge.query.filter_by(name=str(field.data).strip().lower()).all()
    for value in catalogues:
        if value.user == current_user:
            raise ValidationError('У вас уже есть список с таким названием.')
        
        
class AddListForm(FlaskForm):
    list_name = StringField('ListName', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название списка должно содержать только буквы и пробелы.'), validate_list_name])
    submit = SubmitField('Добавить')
            
            
def validate_bookname(form, field):
    if Book.query.filter_by(name=str(field.data).strip().lower()).first():
        raise ValidationError('Данное название книги уже находится в общей базе.')


class AddNewBookForm(FlaskForm):
    isbn = StringField('BookISBN', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Regexp('[0-9-]', 0,
    'Название ISBN должно содержать только цифры и тире.')])
    name = StringField('BookName', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название книги должно содержать только буквы и пробелы.'), validate_bookname])
    author = StringField('AuthorName', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Имя автора должно содержать только буквы и пробелы.')])
    publishing_house = StringField('HouseName', validators=[DataRequired('Поля не должны быть пустыми.'), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название издательсва должно содержать только буквы и пробелы.'), Length(1, 64)])
    description = TextAreaField('Description', validators=[DataRequired('Поля не должны быть пустыми.')])
    release_date = DateField('ReleaseDate')#, format='%d-%m-%Y')
    chapters_count = IntegerField('ChaptersCount', validators=[DataRequired('Поля не должны быть пустыми.'), NumberRange(2, 100, message='Здесь невозможно ошибиться:)')])
    submit = SubmitField('Добавить книгу в базу')
    
