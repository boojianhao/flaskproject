from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.fields import EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError

#custom validation
def validate_name(form,field):
    d=field.data
    if d.isnumeric():
        raise ValidationError("Usename cannot be numeric")

class Login(Form):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SignUp(Form):
    name = StringField('First Name', validators=[validate_name, Optional(), Length(min=2, max=20)])
    email = EmailField('Email*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=8, max=24)])
    confirm_password = PasswordField('Confirm Password*', validators=[DataRequired(), EqualTo(fieldname="password", message="Passwords must match")])
    security_question_1 = StringField('What is your favorite activity?', validators=[DataRequired()])
    security_question_2 = StringField('What is your favorite color?', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class Availablity(Form):
    TIME_RANGE = [
        ("", "default"),
        ("M", "Morning (8:00 AM to 12:00 PM)"),
        ("A", "Afternoon (12:00 PM to 5:00 PM)"),
        ("E", "Evening (5:00 PM to 8:00 PM)"),
    ]

    monday = SelectField(
        "Time Range",
        validators=[DataRequired(message="This question is required")],
        choices=TIME_RANGE,
        default=""
    )
    tuesday = SelectField(
        "Time Range",
        validators=[DataRequired(message="This question is required")],
        choices=TIME_RANGE,
        default=""
    )
    wednesday = SelectField(
        "Time Range",
        validators=[DataRequired(message="This question is required")],
        choices=TIME_RANGE,
        default=""
    )
    thursday = SelectField(
        "Time Range",
        validators=[DataRequired(message="This question is required")],
        choices=TIME_RANGE,
        default=""
    )
    friday = SelectField(
        "Time Range",
        validators=[DataRequired(message="This question is required")],
        choices=TIME_RANGE,
        default=""
    )
    saturday = SelectField(
        "Time Range",
        validators=[DataRequired(message="This question is required")],
        choices=TIME_RANGE,
        default=""
    )
    sunday = SelectField(
        "Time Range",
        validators=[DataRequired(message="This question is required")],
        choices=TIME_RANGE,
        default=""
    )
    submit = SubmitField("Confirm")
