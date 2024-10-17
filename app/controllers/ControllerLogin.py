from app import application, bcrypt, login_required, logout_user, login_user
from flask import render_template, request, flash, redirect, url_for
from app.models import User


@application.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(name=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('register'))
        else:
            flash('Falha no login. Verifique seu nome de usuário e senha.', 'danger')

    return render_template('index.html')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('login'))

