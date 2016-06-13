from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth_route
from .. import db
from .forms import LoginForm, RegisterForm
from ..models import User

@auth_route.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        user = User(email=registerForm.email.data, username=registerForm.username.data, password=registerForm.password.data)
        db.session.add(user)
        flash('You can now login')
        return redirect(url_for('auth_route.login'))
    return render_template('auth/register.html', register=registerForm)

@auth_route.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(username=loginForm.username.data).first()
        if user is not None and user.verify_password(loginForm.password.data):
            login_user(user, loginForm.remember_me.data)
            return redirect(request.args.get('next') or url_for('notes_route.notes'))
        flash('Invalid username or password')
    return render_template('auth/login.html', login=loginForm)

@auth_route.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been logged out')
    return redirect(url_for('auth_route.login'))
