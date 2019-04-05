# -*- coding: utf-8 -*-
from flask import abort, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import or_
from forms import  AddLabortorioForm, EdtLabortorioForm, AddInsumo, EdtInsumo, FmrArtefato, AddArtefatoTipo, AddArtefatoDono
from . import common
from ..models import Laboratorio, Insumo, Artefato, ArtefatoTipo, ArtefatoDono

from .. import db

def check_admin():
	"""
	Prevent a non admin access
	"""
	if not current_user.is_admin:
		abort(403)

def check_PermissionLaboratorioUsuario(laboratorio_id):
	'''
	Prevent for someone without permission access the page 
	'''
	if  current_user.is_admin:
		return None

	laboratorio = Laboratorio.query.filter(or_(Laboratorio.professorTitular_id==current_user.id, 
												Laboratorio.professorSuplente_id==current_user.id), 
											Laboratorio.id==laboratorio_id)
	if not laboratorio:
		abort(403)

@common.add_app_template_filter
def verify_insumos(insumos):
	if all(insumo.quantidadeAtual >= insumo.quantidadeMinima for insumo in insumos):
		return "primary"
	return "danger"

@common.add_app_template_filter
def verify_artefatos(artefatos):
	if all(artefato.status for artefato in artefatos):
		return "primary"
	return "danger"


@common.route('/laboratorios')
@login_required
def list_laboratorios():
	"""
	Render the laboratorios template on the /laboratorios route
	"""
	laboratorios = None
	if current_user.is_admin:
		laboratorios = Laboratorio.query.all()
	else:
		laboratorios = Laboratorio.query.filter(or_(Laboratorio.professorTitular_id==current_user.id, 
												Laboratorio.professorSuplente_id==current_user.id))

	return render_template('common/laboratorios/laboratorios.html', laboratorios=laboratorios, title="Laboratórios").encode('utf-8')
	

@common.route('/laboratorio/adicionar', methods=['GET','POST'])
@login_required
def add_laboratorio():
	"""
	Render the laboratorios template on the /laboratorios route
	"""
	check_admin()
	form = AddLabortorioForm()
	if form.validate_on_submit():
		laboratorio = Laboratorio(descricao=form.descricao.data,
								professorTitular=form.professorTitular_id.data,
								professorSuplente=form.professorSuplente_id.data)
		db.session.add(laboratorio)
		db.session.commit()
		flash('Laboratório adicionado com sucesso!')

		# redireciona para lista de laboratórios
		return redirect(url_for('common.list_laboratorios'))

	return render_template('common/laboratorios/laboratorio.html', form=form, title="Adicionar Laboratório").encode('utf-8')
	
	
@common.route('/laboratorio/editar/<int:lab>', methods=['GET','POST'])
@login_required
def edt_laboratorio(lab):
	"""
	Render the laboratorios template on the /laboratorios route
	"""
	check_admin()

	laboratorio = Laboratorio.query.get_or_404(lab)


	form = EdtLabortorioForm(obj=laboratorio)
	if form.validate_on_submit():
		laboratorio.descricao = form.descricao.data
		laboratorio.professorSuplente = form.professorSuplente.data
		laboratorio.professorTitular = form.professorTitular.data

		db.session.add(laboratorio)
		db.session.commit()
		flash('Laboratório editado com sucesso!')

		# redireciona para lista de laboratórios
		return redirect(url_for('common.list_laboratorios'))

	
	return render_template('common/laboratorios/laboratorio.html', form=form, title="Adicionar Laboratório").encode('utf-8')

@common.route('/insumos/<int:lab>')
@login_required
def list_insumos(lab):
	"""
	Render the Insumo template on the /insumos route
	"""
	check_PermissionLaboratorioUsuario(lab)
	
	insumos = Insumo.query.filter_by(laboratorio_id=lab)
	
	if insumos == None:
		abort(404)

	return render_template('common/insumos/insumos.html', insumos=insumos, lab=lab, title="Insumos").encode('utf-8')
	
@common.route('/insumo/adicionar/<int:lab>', methods=['GET','POST'])
@login_required
def add_insumo(lab):
	"""
	Render the insumo template on the /insumo/adicionar/ route
	"""
	check_PermissionLaboratorioUsuario(lab)

	form = AddInsumo()
	if form.validate_on_submit():
		insumo = Insumo(descricao=form.descricao.data,
								quantidadeAtual=form.quantidadeAtual.data,
								quantidadeMinima=form.quantidadeMinima.data,
								codigoBEC=form.codigoBEC.data,
								laboratorio_id=lab)
		db.session.add(insumo)
		db.session.commit()
		flash('Insumo adicionado com sucesso!')

		# redireciona para lista de insumos
		return redirect(url_for('common.list_insumos', lab=lab))

	return render_template('common/insumos/insumo.html', form=form, add_ism=True, title="Adicionar Insumo").encode('utf-8')

@common.route('/insumo/editar/<int:lab>/<int:insumo>', methods=['GET','POST'])
@login_required
def edt_insumo(lab, insumo):
	"""
	Render the insumo template on the /insumo/editar/ route
	"""
	check_PermissionLaboratorioUsuario(lab)
	insumo = Insumo.query.get_or_404(insumo)

	form = EdtInsumo(obj=insumo)
	
	if form.validate_on_submit():
		insumo.descricao=form.descricao.data
		insumo.quantidadeAtual=form.quantidadeAtual.data
		insumo.quantidadeMinima=form.quantidadeMinima.data
		insumo.codigoBEC=form.codigoBEC.data

		db.session.add(insumo)
		db.session.commit()
		flash('Insumo editado com sucesso!')

		# redireciona para lista de insumos
		return redirect(url_for('common.list_insumos', lab=lab))

	return render_template('common/insumos/insumo.html', form=form, add_ism=False, title="Editar Insumo").encode('utf-8')

@common.route('/artefatos/<int:lab>')
@login_required
def list_artefatos(lab):
	"""
	Render the artefatos template on the /artefatos route
	"""
	check_PermissionLaboratorioUsuario(lab)
	
	artefatos = Artefato.query.filter_by(laboratorio_id=lab)
	
	if artefatos == None:
		abort(404)

	return render_template('common/artefatos/artefatos.html', artefatos=artefatos, lab=lab, title="Artefatos").encode('utf-8')
	

@common.route('/artefato/adicionar/<int:lab>', methods=['GET','POST'])
@login_required
def add_artefato(lab):
	"""
	Render the adicionar template on the /artefato/adicionar route
	"""
	check_PermissionLaboratorioUsuario(lab)
	
	form = FmrArtefato()
	formTipo = AddArtefatoTipo()
	formDono = AddArtefatoDono()

	if form.submit.data and form.validate_on_submit():
		artefato = Artefato(descricao=form.descricao.data,
							capacidade=form.capacidade.data,
							status=form.status.data,
							valorEstimado=form.valorEstimado.data,
							numeroPatrimonio=form.numeroPatrimonio.data,
							artefatoTipo=form.artefatoTipo.data,
							artefatoDono=form.artefatoDono.data,
							laboratorio_id=lab)
							
		db.session.add(artefato)
		db.session.commit()
		flash('Artefato adicionado com sucesso!')

		# redireciona para lista de insumos
		return redirect(url_for('common.list_artefatos', lab=lab))
		
	if formTipo.submitTipo.data and formTipo.validate_on_submit():
		artefatoTipo = ArtefatoTipo(descricao=formTipo.descricao.data)
							
		db.session.add(artefatoTipo)
		db.session.commit()
		flash('Tipo de artefato adicionado com sucesso!')

		form.descricao.data = ''
	
	if formDono.submitDono.data and formDono.validate_on_submit():
		artefatoDono = ArtefatoDono(descricao=formDono.descricao.data)
							
		db.session.add(artefatoDono)
		db.session.commit()
		flash('Dono de artefato adicionado com sucesso!')

		form.descricao.data = ''

	return render_template('common/artefatos/artefato.html', form=form, formTipo=formTipo, formDono=formDono, title="Adicionar Artefato").encode('utf-8')
	
	
@common.route('/artefato/editar/<int:lab>/<int:artefato>', methods=['GET','POST'])
@login_required
def edt_artefato(lab, artefato):
	"""
	Render the editar template on the /artefato/editar route
	"""
	check_PermissionLaboratorioUsuario(lab)
	
	artefato = Artefato.query.get_or_404(artefato)
	formTipo = AddArtefatoTipo()
	formDono = AddArtefatoDono()

	form = FmrArtefato(obj=artefato)
	
	if form.submit.data and form.validate_on_submit():
		artefato.descricao=form.descricao.data
		artefato.capacidade=form.capacidade.data
		artefato.status=form.status.data
		artefato.valorEstimado=form.valorEstimado.data
		artefato.numeroPatrimonio=form.numeroPatrimonio.data
		artefato.artefatoTipo=form.artefatoTipo.data
		artefato.artefatoDono=form.artefatoDono.data
		artefato.laboratorio_id=lab

		db.session.add(artefato)
		db.session.commit()
		flash('Artefato editado com sucesso!')

		# redireciona para lista de artefatos
		return redirect(url_for('common.list_artefatos', lab=lab))
	
	if formTipo.submitTipo.data and formTipo.validate_on_submit():
		artefatoTipo = ArtefatoTipo(descricao=formTipo.descricao.data)
							
		db.session.add(artefatoTipo)
		db.session.commit()
		flash('Tipo de artefato adicionado com sucesso!')
		form.descricao.data = ''
	
	if formDono.submitDono.data and formDono.validate_on_submit():
		artefatoDono = ArtefatoDono(descricao=formDono.descricao.data)
							
		db.session.add(artefatoDono)
		db.session.commit()
		flash('Dono de artefato adicionado com sucesso!')

		form.descricao.data = ''

	return render_template('common/artefatos/artefato.html', form=form, add_art=False, formTipo=formTipo, formDono=formDono, title="Editar Artefato").encode('utf-8')
	
