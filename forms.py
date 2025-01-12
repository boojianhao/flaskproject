from wtforms import Form, StringField, SubmitField, HiddenField, SelectField, FloatField, HiddenField, PasswordField
from wtforms.fields import EmailField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional


class Login(Form):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SignUp(Form):
    name = StringField('First Name', validators=[Optional(), Length(min=2, max=20)])
    email = EmailField('Email*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=8, max=24)])
    confirm_password = PasswordField('Confirm Password*', validators=[DataRequired(), EqualTo(fieldname="password", message="Passwords must match")])
    submit = SubmitField('Sign Up')