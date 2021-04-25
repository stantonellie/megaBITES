from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import InputRequired

class ContactForm(FlaskForm):
    name = TextField("Name")
    email = TextField("Email")
    subject = TextField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])