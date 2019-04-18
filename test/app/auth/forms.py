from flask_wtf import FlaskForm
from peewee import BooleanField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models.user import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in', default=True)
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][\w.]*$',
               message='Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Eamil aleady registed.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist.')
