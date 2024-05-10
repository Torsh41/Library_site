from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange
from wtforms import ValidationError
from ..models import Category, Book


def validate_category_name(form, field):
    categories = Category.query.filter_by(
        name=str(field.data).strip().lower()).all()
    for category in categories:
        if category.name == str(field.data).strip().lower().replace("'", ""):
            raise ValidationError(
                'Такая категория уже имеется.')


class AddCategoryForm(FlaskForm):
    category_name = StringField('CategoryName', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название списка должно содержать только буквы и пробелы.'), validate_category_name])
    
        
class ChangeBookInfoForm(FlaskForm):    
    isbn = StringField('BookISBN', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 64), Regexp('[0-9-]', 0,
    'Название ISBN должно содержать только цифры и тире.')])
    name = StringField('BookName', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название книги должно содержать только буквы и пробелы.')])
    author = StringField('AuthorName', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Имя автора должно содержать только буквы и пробелы.')])
    publishing_house = StringField('HouseName', validators=[DataRequired('Поле не должно быть пустым.'), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название издательсва должно содержать только буквы и пробелы.'), Length(1, 64)])
    release_date = DateField('ReleaseDate', validators=[DataRequired('Поле не должно быть пустым.')])
    chapters_count = IntegerField('ChaptersCount', validators=[DataRequired('Поле не должно быть пустым.'), NumberRange(2, 100, message='Здесь невозможно ошибиться:)')])
    submit = SubmitField('Изменить данные')
    
    def __init__(self, book, *args, **kwargs):
        super(ChangeBookInfoForm, self).__init__(*args, **kwargs)
        self.book = book

    def validate_name(self, name):
        if name.data == self.book.name:
            return True
        book = Book.query.filter_by(name=str(name.data).strip().lower()).first()
        if book and book != self.book:
            raise ValidationError('Название книги, которое вы ввели, уже находится в общей базе.')
  