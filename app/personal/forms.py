from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


class EditProfileForm(FlaskForm):
    avatar = FileField('Photo')
    city = StringField('City', validators=[DataRequired(), Length(1, 64), Regexp('[A-Za-z][A-Za-z]', 0,
    'cities must have only letters')])
    age = IntegerField('Age', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    
