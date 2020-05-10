from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import DataRequired

class loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Sign In")
class signout(FlaskForm):
    logout = SubmitField("Log Out")
class registerform(FlaskForm):
    username = StringField('Desired Username', validators=[DataRequired()])
    password = PasswordField('Desired Password', validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired()])
    classType = SelectField('Class', choices=['Math Edge', 'Reading','Writing','Python','Java','Applied Coding'], validators=[DataRequired()])
    submit = SubmitField("Create")
    logout = SubmitField("Log Out")