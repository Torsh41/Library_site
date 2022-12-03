from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange
from wtforms import ValidationError
from ..models import Cataloge


class EditProfileForm(FlaskForm):
    avatar = FileField('Photo')
    city = StringField('City', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Regexp('[A-Za-z][A-Za-z]', 0,
    'Название города должно содержать только буквы.')])
    age = IntegerField('Age', validators=[DataRequired('Поля не должны быть пустыми.'), NumberRange(1, 100, message='Здесь невозможно ошибиться:)')])
    description = TextAreaField('Description', validators=[DataRequired('Поля не должны быть пустыми.')])
    submit = SubmitField('Сохранить')
    
    
class AddListForm(FlaskForm):
    list_name = StringField('ListName')#, validators=[DataRequired(), Length(1, 64), Regexp('[A-Za-z]', 0,
    #'list name must have only letters')])
    submit = SubmitField('Добавить')
    
    #def validate_catalogue_name(self, field):
        #if Cataloge.query.filter_by(name=field.data).first():
            #raise ValidationError('Catalogue name already in use.')
