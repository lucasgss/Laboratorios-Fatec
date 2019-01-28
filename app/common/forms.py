# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import  PasswordField, StringField, SubmitField, ValidationError, IntegerField, BooleanField, DecimalField
from wtforms.validators import  DataRequired, Email, EqualTo, Length, InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Laboratorio, Usuario, Insumo, ArtefatoTipo, ArtefatoDono

class AddLabortorioForm(FlaskForm):
    """
	Form para adicionar Laboratório
	"""
    descricao = StringField('Descrição', validators=[DataRequired()])
    professorTitular_id = QuerySelectField(label="Professor Titular", validators=[DataRequired()], query_factory=lambda: Usuario.query.all(), get_label="nome") 
    professorSuplente_id = QuerySelectField(label="Professor Suplente", validators=[DataRequired()], query_factory=lambda: Usuario.query.all(), get_label="nome") 
    submit = SubmitField('Adicionar')
    '''
    Verifica se já existe cadastro de Insumo com a mesma desrição.
    '''
    def validate_descricao(self, field):
		if Laboratorio.query.filter_by(descricao=field.data).first():
			raise ValidationError('Laboratório com mesma descrição já criado.')
        
    def validate_professorSuplente(self, field):
        if field.data == self.professorTitular.data:
            raise ValidationError("O professor Suplente deve ser diferente do Titular!")
            
class EdtLabortorioForm(FlaskForm):
    """
	Form para editar Laboratório
	"""
    descricao = StringField('Descrição', validators=[DataRequired()])
    professorTitular = QuerySelectField(label="Professor Titular", validators=[DataRequired()], query_factory=lambda: Usuario.query.all(), get_label="nome") 
    professorSuplente = QuerySelectField(label="Professor Suplente", validators=[DataRequired()], query_factory=lambda: Usuario.query.all(), get_label="nome") 
    submit = SubmitField('Editar')

    def validate_professorSuplente(self, field):
        if field.data == self.professorTitular.data:
            raise ValidationError("O professor Suplente deve ser diferente do Titular!")
            
class AddInsumo(FlaskForm):
    """
	Form para adicionar Insumo
	"""
    descricao = StringField('Descrição', validators=[DataRequired()])
    quantidadeAtual = IntegerField("Quantidade atual", validators=[DataRequired()])
    quantidadeMinima = IntegerField("Quantidade mínima", validators=[DataRequired()])
    codigoBEC =  StringField('Código BEC', validators=[Length(max=30)])
    submit = SubmitField('Salvar')
    '''
    Verifica se já existe cadastro de Insumo com a mesma desrição.
    '''
    def validate_descricao(self, field):
		if Insumo.query.filter_by(descricao=field.data).first():
			raise ValidationError('Insumo com mesma descrição já criado.')
          
class EdtInsumo(FlaskForm):
    """
	Form para editar Insumo
	"""
    descricao = StringField('Descrição', validators=[DataRequired()])
    quantidadeAtual = IntegerField("Quantidade atual", validators=[DataRequired()])
    quantidadeMinima = IntegerField("Quantidade mínima", validators=[DataRequired()])
    codigoBEC =  StringField('Código BEC', validators=[Length(max=30)])
    submit = SubmitField('Salvar')
             
class AddArtefato(FlaskForm):
    """
	Form para adicionar Artefato
	"""     
    descricao = StringField('Descrição', validators=[DataRequired(), Length(max=60)])
    capacidade = StringField('Capacidade', validators=[DataRequired(), Length(max=20)])
    status = BooleanField('Funcional')
    valorEstimado = StringField("Valor estimado", validators=[InputRequired()])
    numeroPatrimonio = StringField('Numero do Patrimônio', validators=[DataRequired(), Length(max=20)])
    artefatoTipo = QuerySelectField(label="Tipo de artefato", validators=[DataRequired()], query_factory=lambda: ArtefatoTipo.query.all(), get_label="descricao") 
    artefatoDono = QuerySelectField(label="Proprietário do artefato", validators=[DataRequired()], query_factory=lambda: ArtefatoDono.query.all(), get_label="descricao") 
    submit = SubmitField('Salvar')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        try:
            float(self.valorEstimado.data)
        except ValueError:
            self.valorEstimado.errors.append(
                'Valor estimado deve ser um numero decimal válido.')
            return False
        return True

        