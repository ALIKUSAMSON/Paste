from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Length, EqualTo

class RegistrationForm(Form):
    username = StringField('Username',validators=[Required(), Length(min=6,max=18)])
    email = StringField('Email',validators=[Required(),Email(message='Invalid address')])
    password = PasswordField('Password',validators=[Required(),Length(min=8, message="Password must be 6 characters as and more"),EqualTo('confirm',message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Sign up')

class LoginForm(Form):
    email = StringField('Email',validators=[Required(),Email(message='Invalid address')])
    password = PasswordField('Password',validators=[Required(), Length(min=8, message="Password must be 6 characters as and more")])
    submit = SubmitField('Sign in')


class ArticleForm(Form):
    title = StringField('Title',validators=[ Length(min=5,max=50)])
    body = TextAreaField('Body',validators=[Length(min=30)])
    submit = SubmitField('Add')
