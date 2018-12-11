# -*- coding: utf-8 -*-
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from . import auth
from forms import LoginForm#, RegistrationForm
from .. import db
from ..models import Usuario


@auth.route('/login', methods=['GET','POST'])
def login():
	"""
	Handle requests to the /login route
	Log an Usuario in through the login form
	"""
	form = LoginForm()
	if form.validate_on_submit():

		# Verifica se o Usuario existe na BD e se a senha bate.
		
		usuario = Usuario.query.filter_by(email=form.email.data).first()
		if usuario is not None and usuario.verify_password(form.password.data):

			# Realiza o login
			login_user(usuario) 

			# Redireciona para a pagina apropriada.
			if usuario.is_admin:
				return redirect(url_for('home.admin_dashboard').encode('utf-8'))
			else:
				return redirect(url_for('common.list_laboratorios').encode('utf-8'))

		# Se os detalhes de login estiverem errados.
		else:
			flash('Dados de login invalidos!'.decode('utf-8'))

	# load login template
	return render_template('auth/login.html', form=form, title='Login').encode('utf-8')

@auth.route('/logout')
@login_required
def logout():
	"""
	Handle requests to the /logout route
	Log an employee out through the logout link
	"""
	logout_user()
	flash('Logout realizado com sucesso!')

	# redirect to the login page
	return redirect(url_for('auth.login'))

# @auth.route('/register', methods=['GET','POST'])
# def register():
# 	"""
# 	Handle request to the /register route
# 	Sdd an employee to the database through registration form 
# 	"""
# 	form = RegistrationForm()
# 	if form.validate_on_submit():
# 		employee = Employee(email=form.email.data,
# 							username=form.username.data,
# 							first_name=form.first_name.data,
# 							last_name=form.last_name.data,
# 							password=form.password.data)

# 		# add an employee to the database
# 		db.session.add(employee)
# 		db.session.commit()
# 		flash('You have successfully registered! You may now log in.')

# 		# redirect to the login page
# 		return redirect(url_for('auth.login'))

# 	return render_template('auth/register.html', form=form, title='Register')
