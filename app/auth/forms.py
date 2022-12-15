from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, Length
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Email('Неверный email адрес.')])
    username = StringField('Username', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Regexp('[A-Za-zА-Яа-яЁё0-9_.]', 0,
'Логин содержит только буквы, цифры, точки или символы подчеркивания.')])
    password = PasswordField('Password', validators=[DataRequired('Поля не должны быть пустыми.'), EqualTo('password2', message='Пароли должны совпадать.'), Length(6, 20, message='Пароль должен быть от 6 до 20 символов включительно.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired('Поля не должны быть пустыми.')])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email уже зарегистрирован.')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Данное имя пользователя уже используется.')
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Email('Неверный email адрес.')])
    password = PasswordField('Password', validators=[DataRequired('Поля не должны быть пустыми.')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
    

class ChangePasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Поля не должны быть пустыми.'), Length(1, 64), Email('Неверный email адрес.')])
    password = PasswordField('New password', validators=[DataRequired('Поля не должны быть пустыми.'), EqualTo('password2', message='Пароли должны совпадать.')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired('Поля не должны быть пустыми.')])
    submit = SubmitField('Update Password')