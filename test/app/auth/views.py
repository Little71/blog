from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm
from app.models.user import User
from app.models.base import db


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.default)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        with db.auto_commit():
            user = User()
            print(request.form)
            user.set_attr(request.form)
            db.session.add(user)
        flash('you can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
