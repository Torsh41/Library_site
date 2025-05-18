from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, URL, Optional
from wtforms import ValidationError
from ..models import Category, Book
from isbnlib import is_isbn10, is_isbn13
from app.personal.forms import AddNewBookForm, validate_isbn_10_or_13


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
        

# Account for a case when field does not change
def validate_bookname(form, field):
    existing_book = Book.query.filter_by(name=str(field.data).strip().lower()).first()
    if existing_book is not None and existing_book.id != form.book.id:
        raise ValidationError('Данное название книги уже находится в общей базе.')

# Account for a case when field does not change
def validate_isbn(form, field):
    existing_book = Book.query.filter_by(name=str(field.data).strip().lower()).first()
    if existing_book is not None and existing_book.id != form.book.id:
        raise ValidationError('Книга с таким ISBN уже находится в общей базе.')


# This form is almost identical to app.personal.forms.AddNewBookForm. 
# Unique constraint validation methods have to be redefined.
class ChangeBookInfoForm(AddNewBookForm): 
    isbn = StringField('BookISBN', validators=[Optional(), Length(1, 128), validate_isbn, validate_isbn_10_or_13])
    name = StringField('BookName', validators=[DataRequired('Поле не должно быть пустым.'), Length(1, 128), Regexp('[A-Za-zА-Яа-яЁё ]', 0,
    'Название книги должно содержать только буквы и пробелы.'), validate_bookname])
    submit = SubmitField('Изменить данные')
    
    def __init__(self, book, *args, **kwargs):
        super(ChangeBookInfoForm, self).__init__(*args, **kwargs)
        self.book = book

  
