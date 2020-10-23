from flask import Blueprint, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(email = email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.login'))
    
    login_user(user, remember = remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup', methods = ['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email = email).first()
    
    if user:
        flash('Email address already exists')
        return redirect(url_for('main.signup'))
    
    new_user = User(email = email, name = name, password = generate_password_hash(password, method = 'sha256'))
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('main.login'))

@auth.route('/logout')
def logout():
    return 'Logout'
