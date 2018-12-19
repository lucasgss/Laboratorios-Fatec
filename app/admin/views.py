# -*- coding: utf-8 -*-
from flask import abort, flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import admin 
from forms import AdicionarUsuario, EditarUsuario
from .. import db
from ..models import Usuario# Usuario


def check_admin():
	"""
	Prevent a non admin access
	"""
	if not current_user.is_admin:
		abort(403)
					   
@admin.route('/usuarios')
@login_required
def list_usuarios():
	"""
	List all usuarios
	"""
	check_admin()
	usuarios = Usuario.query.all()
	return render_template('admin/usuarios/usuarios.html', usuarios=usuarios, title='Usuários'.decode('utf-8')).encode('utf-8')

@admin.route('/usuarios/adicionar', methods=['GET','POST'])
@login_required
def add_usuario():
	"""
	Handle request to the /usuario/adicionar
	Add um usuario através do registration form 
	"""
	check_admin()
	form = AdicionarUsuario()
	if form.validate_on_submit():
		isadmin = (form.papel.data == "Administrador")
		usuario = Usuario(nome=form.nome.data,
						email=form.email.data,
						password=form.password.data,
						denominacao=form.denominacao.data,
						papel=form.papel.data,
						is_admin=isadmin)
		# adiciona o Usuario na BD
		db.session.add(usuario)
		db.session.commit()
		flash('Usuario adicionado com sucesso!')

		# redireciona para lista de usuarios
		return redirect(url_for('admin.list_usuarios'))

	return render_template('admin/usuarios/usuario.html', form=form, title='Usuários'.decode('utf-8')).encode('utf-8')


@admin.route('/usuarios/editar/<int:id>', methods=['GET','POST'])
@login_required
def edt_usuario(id):
	"""
	Handle request to the /usuario/editar
	Edita um usuario através do registration form 
	"""
	check_admin()

	usuario = Usuario.query.get_or_404(id)

	form = EditarUsuario(obj=usuario)
	if form.validate_on_submit():
		isadmin = (form.papel.data.id == 2)
		usuario.nome=form.nome.data
		usuario.email=form.email.data
		if form.password.data != "":
			usuario.password=form.password.data
		usuario.denominacao=form.denominacao.data
		usuario.papel=form.papel.data
		usuario.is_admin=isadmin
		
		db.session.add(usuario)
		db.session.commit()
		flash('Usuario editado com sucesso!')

		# redireciona para lista de usuarios
		return redirect(url_for('admin.list_usuarios'))

	form.confirmar_email.data = usuario.email

	return render_template('admin/usuarios/usuario.html', add_usr=False, form=form, title='Editar usuários'.decode('utf-8')).encode('utf-8')
