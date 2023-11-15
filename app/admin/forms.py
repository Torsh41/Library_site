from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms import ValidationError
from ..models import Category


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
