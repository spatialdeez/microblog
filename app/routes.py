from flask import render_template, flash, redirect, url_for, request
from datetime import datetime, timezone
from app import app
from app.forms import LogInForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required # type: ignore
import sqlalchemy as sa # type: ignore
from app import db
from app.models import User
from urllib.parse import urlsplit


# The @ symbol is a decorator!
# It modifies the function that follows it. In this case, it registers the function as a route handler for the specified URL path.
@app.route('/') # This decorator registers the function as a route handler for the URL path "/"

@app.route('/index') # This decorator registers the function as a route handler for the URL path "/index"
@login_required # type: ignore
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'I hope to see you in France!',
        },

        {
            'author': {'username': 'Susan'},
            'body': 'Love the weather today!',
        }

    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) # Let the user in the main page
    form = LogInForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user) # Collect user data and do a push
        db.session.commit() # Commits the above session to the database
        flash('Successfully registered as a user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Text post 1'},
        {'author': user, 'body': 'Text post 2'},
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()