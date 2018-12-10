# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import  PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import  DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Usuario, Papel


class AdicionarUsuario(FlaskForm):
	"""
	Form para adicionar Usuario
	"""
	nome = StringField('Nome', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), 
									Email(),
									EqualTo('confirmar_email')])
	confirmar_email = StringField('Confirmar email', validators=[DataRequired(), Email()])
	password = PasswordField('senha', validators=[
									DataRequired(),
									EqualTo('confirmar_senha')
									])
	confirmar_senha = PasswordField('Confirmar senha')
	denominacao = StringField("Denominação".decode('utf-8'),validators=[DataRequired()], default="Professor")
	papel = QuerySelectField(validators=[DataRequired()], query_factory=lambda: Papel.query.all(), get_label="descricao")
	submit = SubmitField('Adicionar')
	
	def validate_email(self, field):
		if Usuario.query.filter_by(email=field.data).first():
			raise ValidationError('Email já em uso.'.decode('utf-8'))

			
class EditarUsuario(FlaskForm):
	"""
	Form para editar Usuario
	"""
	nome = StringField('Nome', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), 
									Email(),
									EqualTo('confirmar_email')])
	confirmar_email = StringField('Confirmar email', validators=[DataRequired()])
	password = PasswordField('senha', validators=[
									EqualTo('confirmar_senha')
									])
	confirmar_senha = PasswordField('Confirmar senha')
	denominacao = StringField("Denominação".decode('utf-8'),validators=[DataRequired()], default="Professor")
	papel = QuerySelectField(validators=[DataRequired()], query_factory=lambda: Papel.query.all(), get_label="descricao")
	submit = SubmitField('Editar')