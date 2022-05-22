from flask_wtf import FlaskForm
from Trivia.models import User
from wtforms import (BooleanField, FieldList, FormField, PasswordField,
                     StringField, SubmitField, TextAreaField, ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=32)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        #check it is filled out or not 
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        # user exist 
        if not user:
            self.username.errors.append('Unknown username')
            return False
        # check password
        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('Verify password',
                            validators=[DataRequired(), EqualTo('password',
                                                                message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        #check it is filled out or not 
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        # check for Username already registered
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        # check for email already registered 
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class EditProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=32)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        # to prevent duplicate username
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class QuestionForm(FlaskForm):
    anwser = StringField('Awnser', validators=[DataRequired()])
    submit = SubmitField('Next')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
