from wtforms.fields import StringField,PasswordField,SubmitField
from flask_wtf import FlaskForm   #Imports the main class to manage Forms
from wtforms.validators import DataRequired      #Imports the validators
class LoginForm(FlaskForm):
    username = StringField('User Name',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    label = StringField('Label', validators = [DataRequired()])
    link_to_reference = StringField('Link to content', validators = [DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    submit = SubmitField('Submit')


#Home Buttons
class InitialAddForm(FlaskForm):
    submit = SubmitField('Agregar')

class InitialSearchForm(FlaskForm):
    submit = SubmitField('A Pistear!')

class InitialRateForm(FlaskForm):
    submit = SubmitField('Opinar')


#Forms

#New place
class AddForm(FlaskForm):
    text = StringField("", validators=[DataRequired()])
    
    submit = SubmitField('Siguiente')

class SearchForm(FlaskForm):
    text = StringField("", validators=[DataRequired()])
    
    submit = SubmitField('Siguiente')

class RateForm(FlaskForm):
    text = StringField("", validators=[DataRequired()])
    
    submit = SubmitField('Siguiente')


class UpdateTaskForm(FlaskForm):
    submit = SubmitField('Entregar')