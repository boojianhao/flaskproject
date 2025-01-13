from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class Login(Form):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SignUp(Form):
    name = StringField('First Name', validators=[Optional(), Length(min=2, max=20)])
    email = EmailField('Email*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=8, max=24)])
    confirm_password = PasswordField('Confirm Password*', validators=[DataRequired(), EqualTo(fieldname="password", message="Passwords must match")])
    security_question_1 = StringField('What is your favorite activity?', validators=[DataRequired()])
    security_question_2 = StringField('What is your favorite color?', validators=[DataRequired()])
    submit = SubmitField('Sign Up')