from wtforms.fields import StringField,PasswordField,SubmitField
from flask_wtf import FlaskForm   #Imports the main class to manage Forms
from wtforms.validators import DataRequired      #Imports the validators
class LoginForm(FlaskForm):
    username = StringField('User Name',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')