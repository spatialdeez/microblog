from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField # type: ignore
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length # type: ignore
import sqlalchemy as sa # type: ignore
from app import db
from app.models import User

class LogInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me next time')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) # Username that is required to be filled
    email = StringField('Email', validators=[DataRequired()]) # Email that is required to be filled
    password = PasswordField('Password', validators=[DataRequired()]) # Passowrd that is required to be filled
    password_repeat = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')]) # Confirm passowrd that is required to be filled and equal to the variable, 'password' 
    submit = SubmitField('Create account') # Interactive submit button 

    def validate_username(self, username): # Adds another stock validator that validates usernames
        user = db.session.scalar(sa.select(User).where(User.username == username.data)) # Filters out for specific username given in the parameters
        if user is not None:
            raise ValidationError('Username take! Please use a different username.')
        
    def validate_email(self, email): # Adds another stock validator that validates email
        user = db.session.scalar(sa.select(User).where(User.email == email.data)) # Filters out for specific email given in the parameters
        if user is not None:
            raise ValidationError('Email already registered. Please use a different email address.')
        
class ProfileEditorForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    about_me = StringField('About me:', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save changes')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
            
class EmptyForm(FlaskForm):
    submit = SubmitField('submit')

class PostForm(FlaskForm):
    post = TextAreaField('Say something...', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Post')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset your password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[DataRequired()])
    password2 = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Confirm')