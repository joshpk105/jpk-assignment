import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, SubmitField, FieldList
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Author, Book, Ownership
from flask_login import current_user

collapse = re.compile(r'\s+')

class NewBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    #purchase = DateTimeField('Purchase Date')
    # Not sure how to allow for more or less entries dynamically
    authors = FieldList(StringField('Author'), min_entries=5)
    note = StringField('Note')
    submit = SubmitField('Add Book')

    def validate_authors(self, authors):
        max_len = 0
        for a in authors:
            a.data = collapse.sub(' ', a.data.strip())
            max_len = max(max_len, len(a.data))
        if max_len == 0:
            raise ValidationError('Please enter at least one author.')
    
    def validate_title(self, title):
        title.data = collapse.sub(' ', title.data.strip())
        if len(title.data) == 0:
            raise ValidationError('Please enter a title.')
    
        