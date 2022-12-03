from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    find_result = StringField(validators=[DataRequired(message='Обязательное поле')])
    find_result_submit = SubmitField('search')