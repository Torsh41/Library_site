from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, URL, Optional
from wtforms import ValidationError
from ..models import Category, Book, ModerationRequest


class BookSearchFiltersForm(FlaskForm):
    bookname = StringField(validators=[Optional()])
    username = StringField(validators=[Optional()])
    category = SelectField("CategoryId", validators=[Optional()])
    status = SelectField("ModerationStatus", validators=[Optional()])
    # submit = SubmitField()
    
    def __init__(self, category_list=[], *args, **kwargs):
        super(BookSearchFiltersForm, self).__init__(*args, **kwargs)
        self.update_category_choises(category_list)
        self.update_status_choises()

    def update_category_choises(self, category_list):
        self.category.choices = [("", "любая категория")] + category_list

    def update_status_choises(self):
        # To set default value, assumes ModerationRequest.STATUS_OPEN == 0
        self.status.choices = [("", "любой статус")] + list(ModerationRequest.status_dict.items())


class SetModerationStatusForm(FlaskForm):
    book_id = IntegerField("BookId",
                    validators=[DataRequired("Отсутствует параметр book_id...")])
    comment = TextAreaField("ModerationComment",
                    validators=[Optional(), Length(max=128)])
    status = SelectField("ModerationStatus",
                    choices=list(ModerationRequest.status_dict.items()),
                    validators=[DataRequired("Отсутствует параметр status...")])

    def _comment(self, **kwargs):
        # Set default value of TextAreaField
        if kwargs["default"]:
            self.comment.process_data(kwargs["default"])
        return self.comment(**kwargs)


