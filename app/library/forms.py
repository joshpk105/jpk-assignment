import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields import DateField, EmailField
from app.models import Author, Book, Ownership
from flask_login import current_user

collapse = re.compile(r'\s+')

class SendLibraryForm(FlaskForm):
    recipient = EmailField('Email Library', validators=[DataRequired()])
    send = SubmitField("Send")

class BookForm(FlaskForm):
    title = StringField('Title', validators=[])
    purchase = DateField('Purchase Date', format='%Y-%m-%d')
    # Not sure how to allow for more or less entries dynamically
    authors = FieldList(StringField('Author'), min_entries=5)
    note = StringField('Note')

    def validate_authors(self, authors):
        max_len = 0
        for a in authors:
            a.data = collapse.sub(' ', a.data.strip())
            max_len = max(max_len, len(a.data))
            # Need to check whether len() counts bytes
            # and if the db handles it the same way
            if len(a.data) > 200:
                raise ValidationError('Author name too long.')
        if max_len == 0:
            raise ValidationError('Please enter at least one author.')
    
    def validate_title(self, title):
        title.data = collapse.sub(' ', title.data.strip())
        if len(title.data) == 0:
            raise ValidationError('Please enter a title.')
        # Need to check whether len() counts bytes
        # and if the db handles it the same way
        if len(title.data) > 120:
            raise ValidationError('Title too long.')

    def validate_purchase(self, purchase):
        if purchase.data is None:
            raise ValidationError("Please enter a purchase date.")

class NewBookForm(BookForm):
    submit = SubmitField('Add Book')

class EditBookForm(BookForm):
    submit = SubmitField("Edit Book")

    # If title is empty we delete the book
    def validate_title(self, title):
        title.data = collapse.sub(' ', title.data.strip())
        if len(title.data) > 120:
            raise ValidationError('Title too long.')
    
        