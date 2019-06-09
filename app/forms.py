from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False
    trn = StringField('trn', validators=[InputRequired(), Length(min=9, max=9)])
    username = StringField('username', validators=[InputRequired()])
    password = StringField('password', validators=[InputRequired(), 
                EqualTo('confirm_password', message="Passwords must match.")])
    confirm_password = StringField('confirm_password')
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    phone = StringField('phone', validators=[InputRequired(), Length(min=10, max=10)])
    address = StringField('address', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = StringField('password', validators=[InputRequired()])
    
class PostForm(FlaskForm):
    user_trn = StringField('user_trn', validators=[InputRequired(), Length(min=9, max=9)])
    title = StringField('title', validators=[InputRequired()])
    content = StringField('content', validators=[InputRequired()])
    