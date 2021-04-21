from app import app
from flask import render_template, flash, redirect, request, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from app.forms import LoginForm


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid User Name or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@ app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@ app.route('/index')
@ login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'A story about penguins'
        },
        {
            'author': {'username': 'Anla'},
            'body': 'Once upon a time in the bleast'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)
