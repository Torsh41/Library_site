from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange
from wtforms import ValidationError
from ..models import Book, Cataloge, DiscussionTopic, Category
from flask_login import current_user


def validate_topic_name(form, field): 
    print(field)
    category = Category.query.filter_by(name=str(field.name)).first()
    for topic in category.topics.all():
        if topic.name == str(field.data):
            raise ValidationError('Такая тема уже имеется.')


class AddTopicForm(FlaskForm):
    topic_name = StringField('TopicName', validators=[Length(1, 1024), validate_topic_name])

