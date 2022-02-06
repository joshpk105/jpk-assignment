from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, SubmitField, FieldList
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Author, Book, Ownership
from flask_login import current_user

class NewBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    #purchase = DateTimeField('Purchase Date')
    authors = FieldList(StringField('Author'), min_entries=1)
    note = StringField('Note')
    submit = SubmitField('Add Book')
        