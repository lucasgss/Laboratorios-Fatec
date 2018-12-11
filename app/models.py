# -*- coding: latin-1 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
class Usuario(UserMixin, db.Model):
	"""
	Criando tabela usuarios
	"""

	__tablename__='usuario'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), index=True, unique=True)
	nome = db.Column(db.String(150), index=True, nullable=False)
	senha_hash = db.Column(db.String(128), nullable=False)
	denominacao = db.Column(db.String(20))
	papel_id = db.Column(db.Integer, db.ForeignKey('papel.id'), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	

	@property
	def password(self):
		"""
		Prevent password from being accessed
		"""
		raise AttributeError('Senha não é um atributo legível!')

	@password.setter
	def password(self, password):
		# Set Password to a hashed password
		self.senha_hash = generate_password_hash(password)

	def verify_password(self, password):
		"""
		Check if hashed password matches actual password 
		"""
		return check_password_hash(self.senha_hash, password)

	def __repr__(self):
		return "<Usuario: {}>".format(self.nome)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
	return Usuario.query.get(int(user_id))

class Papel(db.Model):

	__tablename__ = 'papel'
	id = db.Column(db.Integer, primary_key=True)
	descricao = db.Column(db.String(60), unique=True)
	usuarios = db.relationship('Usuario', backref='papel', lazy='dynamic')

	def __repr__(self):
		return '<Papel: {}>'.format(self.descricao)

class Laboratorio(db.Model):

	__tablename__ = 'laboratorio'
	id = db.Column(db.Integer, primary_key=True)
	descricao = db.Column(db.String(60), unique=True)
	auditado = db.Column(db.Boolean, default=False)
	professorTitular_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
	professorSuplente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
	
	professorTitular = db.relationship("Usuario",foreign_keys=[professorTitular_id], backref="laboratoriosTitular", uselist=False)
	professorSuplente = db.relationship("Usuario",foreign_keys=[professorSuplente_id], backref="laboratoriosSuplente", uselist=False)

	def __repr__(self):
		return '<Laboratorio: {}>'.format(self.descricao)

class Insumo(db.Model):

	__tablename__ = 'insumo'
	id = db.Column(db.Integer, primary_key=True)
	descricao = db.Column(db.String(60), unique=True)
	quantidadeAtual = db.Column(db.Integer)
	quantidadeMinima = db.Column(db.Integer)
	descricao = db.Column(db.String(60))
	laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorio.id'))
	laboratorio = db.relationship('Laboratorio', uselist=False)

	def __repr__(self):
		return '<Insumo: {}>'.format(self.descricao)

class ArtefatoTipo(db.Model):

	__tablename__ = 'artefatoTipo'
	id = db.Column(db.Integer, primary_key=True)
	descricao = db.Column(db.String(60), unique=True)

	def __repr__(self):
		return '<Artefato tipo: {}>'.format(self.descricao)

class ArtefatoDono(db.Model):

	__tablename__ = 'artefatoDono'
	id = db.Column(db.Integer, primary_key=True)
	descricao = db.Column(db.String(60), unique=True)

	def __repr__(self):
		return '<artefato dono: {}>'.format(self.descricao)

class Artefato(db.Model):

	__tablename__ = 'artefato'
	id = db.Column(db.Integer, primary_key=True)
	descricao = db.Column(db.String(60), unique=True)
	capacidade = db.Column(db.String(20), nullable=False)
	status = db.Column(db.Boolean, nullable=False)
	valorEstimado = db.Column(db.DECIMAL(13,2))
	numeroPatrimonio = db.Column(db.String(20), nullable=False)
	laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorio.id'), nullable=False)
	artefatoTipo_id = db.Column(db.Integer, db.ForeignKey('artefatoTipo.id'), nullable=False)
	artefatoDono_id = db.Column(db.Integer, db.ForeignKey('artefatoDono.id'), nullable=False)

	def __repr__(self):
		return '<Artefato: {}>'.format(self.descricao)
