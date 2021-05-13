from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('base.html', user=current_user)

@views.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password',category='error')
                return redirect(url_for('views.login'))
        else:
            flash('Email does not exist',category='error')
            return redirect(url_for('views.login'))
    else:
        return render_template('login.html', user=current_user)

@views.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        c_password = request.form.get('c_password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
            return redirect(url_for('views.reg'))
        elif len(name) < 3:
            flash('Enter a proper name', category='error')
            return redirect(url_for('views.reg'))
        elif len(password) < 5:
            flash('Password should contain atleast 5 character', category='error')
            return redirect(url_for('views.reg'))
        elif password != c_password:
            flash('Passwod and Confirm password are not matching', category='error')
            return redirect(url_for('views.reg'))
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.login'))

    else:
        return render_template('register.html', user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))