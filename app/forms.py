from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SelectField, TextAreaField, SubmitField, BooleanField, \
	StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class SubmissionForm(FlaskForm):
	language = SelectField('Language', validators=[DataRequired()])
	source_code = TextAreaField()
	custom_input_check = BooleanField('Custom Input')
	compile_code = SubmitField('Compile It')
	run_code = SubmitField('Run It')
	custom_input = TextAreaField()
	save_code = SubmitField('Save')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	recaptcha = RecaptchaField()
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Password2', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address')