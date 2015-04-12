from flask_wtf import Form

from project.models import Category
from wtforms import TextField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length

CATEGORIES = [category.title.encode("utf8")
              for category in Category.query.all()]


class WebinarCreateForm(Form):
    title = TextField(
        'title', validators=[DataRequired()])
    description = TextAreaField(
        'description', validators=[DataRequired()])
    category = SelectField(
        'category', choices=[(c, c) for c in CATEGORIES], validators=[DataRequired()])


class WebinarEditForm(Form):
    title = TextField(
        'title', validators=[DataRequired()])
    description = TextAreaField(
        'description', validators=[DataRequired()])
