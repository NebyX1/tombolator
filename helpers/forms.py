from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	name = StringField(label = 'User Name:', validators = [DataRequired()])
	password = PasswordField(label = 'Password:', validators = [DataRequired()])
	submit = SubmitField(label='Sign in')