# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Usuario

class LoginForm(FlaskForm):
	"""
	Form para fazer login
	"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Senha', validators=[DataRequired()])
	submit = SubmitField('Login')

# class RegistrationForm(FlaskForm):
# 	"""
# 	Form para usauarios criarem uma nova conta
# 	"""
# 	email = StringField('Email', validators=[DataRequired(), Email()])
# 	"""username = StringField('Username', validators=[DataRequired()])"""
# 	first_name = StringField('Nome', validators=[DataRequired()])
# 	last_name = StringField('Sobrenome', validators=[DataRequired()])
# 	password = PasswordField('senha', validators=[
# 										DataRequired(),
# 										EqualTo('confirm_password')
# 										])
# 	confirm_password = PasswordField('Confirmar senha')
# 	submit = SubmitField('Register')

# 	def validate_email(self, field):
# 		if Employee.query.filter_by(email=field.data).first():
# 			raise ValidationError('Email is already in use.')
# """
# 	def validate_username(self, field):
# 		if Employee.query.filter_by(username=field.data).first():
# 			raise ValidationError('Username is already in use.')"""
