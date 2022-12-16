from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
 body = StringField('', validators=[DataRequired('Заполните поле!')])
 submit = SubmitField('Отправить')