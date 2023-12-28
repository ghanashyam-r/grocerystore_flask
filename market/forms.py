
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    
    def validate_username(self, usernamecheck):
        user = User.query.filter_by(username=usernamecheck.data).first()
        if user:
            raise ValidationError('Username already taken! Please try a different username')

    def validate_email_address(self, email_addresscheck):
        email_address = User.query.filter_by(email=email_addresscheck.data).first()
        if email_address:
            raise ValidationError('Email Address already in Use! Please try a different email address')
        
        
    username = StringField(label='User Name:',validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:',validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:',validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in') 

class EditCategoryForm(FlaskForm):
    new_name = StringField(label='Category Name:', validators=[DataRequired()])
    submit = SubmitField(label='Update Category')    