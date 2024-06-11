from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange
from wtforms import ValidationError
from ..models import Book
from isbnlib import is_isbn10, is_isbn13


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё0-9_.]', 0, 'Логин содержит только буквы, цифры, точки или символы подчеркивания.')])
    avatar = FileField('Photo')
    city = StringField('City', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название города должно содержать только буквы и пробелы.')])
    age = IntegerField('Age', validators=[DataRequired('Поле не должно быть пустым.'), NumberRange(1, 100, message='Здесь невозможно ошибиться:)')])
    submit = SubmitField('Сохранить')
    
              
def validate_bookname(form, field):
    if Book.query.filter_by(name=str(field.data).strip().lower()).first():
        raise ValidationError('Данное название книги уже находится в общей базе.')
    

def validate_isbn(form, field):
    if Book.query.filter_by(isbn=field.data).first():
        raise ValidationError('Книга с таким ISBN уже находится в общей базе.')


def validate_isbn_10_or_13(form, field):
    if not is_isbn10(field.data) and not is_isbn13(field.data):
        raise ValidationError('ISBN должен соответствовать стандарту ISBN 10 или ISBN 13.')
    
    
class AddNewBookForm(FlaskForm):
    isbn = StringField('BookISBN', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 128), validate_isbn, validate_isbn_10_or_13])
    name = StringField('BookName', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 128), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название книги должно содержать только буквы и пробелы.'), validate_bookname])
    author = StringField('AuthorName', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 128), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Имя автора должно содержать только буквы и пробелы.')])
    publishing_house = StringField('HouseName', validators=[DataRequired('Поле не должно быть пустым.'), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название издательсва должно содержать только буквы и пробелы.'), Length(1, 64)])
    description = TextAreaField('Description', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 1024)])
    release_date = DateField('ReleaseDate', validators=[DataRequired('Поле не должно быть пустым.')])
    chapters_count = IntegerField('ChaptersCount', validators=[DataRequired('Поле не должно быть пустым.'), NumberRange(2, 100, message='Здесь невозможно ошибиться:)')])
    submit = SubmitField('Добавить книгу в базу')
    
