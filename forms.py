from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import InputRequired

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    subject = StringField("Subject", validators=[InputRequired()])
    message = TextAreaField("Message", validators=[InputRequired()])
    submit = SubmitField("Send")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])