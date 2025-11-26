# WTForms for user authentication and registration.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from ..models import User


# user registration form
class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    role = SelectField(
        "Role",
        choices=[("doctor", "Doctor"), ("nurse", "Nurse")],
        validators=[DataRequired()],
    )

    submit = SubmitField("Register")

 
 # form for user login
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


#  form for deleting a user
class DeleteUserForm(FlaskForm):
    pass
