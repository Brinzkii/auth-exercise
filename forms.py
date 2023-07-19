from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])
    email = StringField("Email", validators=[InputRequired(), Length(max=50)])
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class DeleteForm(FlaskForm):
    """Form confirming delete user and all associated feedback"""

    delete = SelectField(
        "Delete user and all associated feedback?",
        choices=[(True, "Yes"), (False, "No")],
        validators=[InputRequired()],
    )


class FeedbackForm(FlaskForm):
    """Form for submitting feedback"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Content", validators=[InputRequired()])
