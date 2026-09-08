from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import OperationalError

from app.models.user import User

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("Usuario recibido:", username)
        print("Password recibido:", password)
        user = User.query.filter_by(username=username).first()
        print("Usuario encontrado:", user)
        if user:
            print("Password correcto:", user.check_password(password))
        if user and user.check_password(password):
            login_user(user)
            print("Usuario autenticado:", current_user.is_authenticated)
            print("Usuario actual:", current_user)
            return redirect(url_for('dashboard.index'))
        flash('Usuario o contraseña incorrectos')
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
"""
from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from app.models.user import User

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.check_password(password):

            login_user(user)

            return redirect(
                url_for('dashboard.index')
            )

        flash('Usuario o contraseña incorrectos')

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('auth.login'))
"""