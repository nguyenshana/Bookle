from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError,HiddenField,BooleanField, RadioField
from wtforms.validators import DataRequired, Email, DataRequired, EqualTo

class SearchForm(FlaskForm):
    bookName = StringField('Book Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
