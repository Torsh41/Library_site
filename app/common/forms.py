from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, URL, Optional
from wtforms import ValidationError
from app import database
from app.models import Category, ModerationRequest


# TODO: use this form in category_page.html and admin_panel.html
class BookSearchForm(FlaskForm):
    page = IntegerField()
    bookname = StringField(validators=[Optional(), Length(1, 128)])
    author = StringField(validators=[Optional(), Length(1, 128)])
    publishing_house = StringField('housename', validators=[Optional(), Length(1, 64)])
    description = TextAreaField(validators=[Optional(), Length(1, 1024)])
    release_year_min = StringField('releaseyearmin', validators=[Optional(), Length(max=4), Regexp('[0-9]')])
    release_year_max = StringField('releaseyaermax', validators=[Optional(), Length(max=4), Regexp('[0-9]')])
    category = SelectField("CategoryId", validators=[Optional()])
    username = StringField(validators=[Optional()])
    status = SelectField("ModerationStatusId", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.update_category_choises()
        self.update_status_choises()

    def update_category_choises(self):
        category_list = database.session.execute(
                database.select(Category).order_by(Category.name)
        ).scalars().all()
        category_select_list = [(cy.id, cy.name) for cy in category_list]
        self.category.choices = [("", "любая категория")] + category_select_list

    def update_status_choises(self):
        # To set default value, assumes ModerationRequest.STATUS_OPEN == 0
        self.status.choices = [("", "любой статус")] + list(ModerationRequest.status_dict.items())
