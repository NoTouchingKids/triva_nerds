# Flask import
from flask import Flask, Blueprint, redirect, url_for, render_template, request, jsonify, flash, g
from flask import render_template_string
from flask_login import current_user, login_required, login_user, logout_user

# All Trivia imports
from Trivia import app, db
from Trivia.models import TrivaQuestion, User
# Utility imports
#from werkzeug import check_password_hash
import json
from werkzeug.security import generate_password_hash

# 
from Trivia.scripts.forms import LoginForm, RegisterForm


@app.route('/')
@app.route('/index')
def index():
    # ...
    return render_template("index.html", title='Home Page')


# -------- Login ------------------------------------------------------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    print(f'validate: <{form.validate_on_submit()}>     User: <{form.username.data}>    password: <{form.password.data}>')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('game'))
    return render_template('login.html', title='Sign In', form=form)

# -------- logout---------------------------------------------------------- #
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# -------- Signup ---------------------------------------------------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        print(1)
        return redirect(url_for('index'))
    form = RegisterForm()
    print(f'validate: <{form.validate_on_submit()}>     User: <{form.username.data}>    password: <{form.password.data}>')
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        print(user)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# -------- Settings ---------------------------------------------------------- #

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
# -------- Game ---------------------------------------------------------- #
@app.route('/game')
def game():
    q1 = TrivaQuestion.get_questions()
    for i in range(len(q1)):
        q1[i] = q1[i].Questions
    print(len(q1))
    return render_template('game.html', questions=q1)
# -------- testing ---------------------------------------------------------- #


incomes = [
    {'description': 'salary', 'amount': 5000}
]

@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204


@app.route('/questions')
def questions():
    q1 = TrivaQuestion().get_questions(10)
    for i in range(len(q1)):
        q1[i] = q1[i].Questions
    return jsonify(q1)

@app.route('/all_user')
def user_all():
    user = User.query.all()
    print(user[2])
    return '', 204

