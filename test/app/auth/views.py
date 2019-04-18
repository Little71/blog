from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user

from app.auth import auth
from app.auth.forms import LoginForm
from app.models.user import User



@auth.route('/login')
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
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
