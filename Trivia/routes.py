# Flask import
from datetime import datetime
from flask import Flask, Blueprint, redirect, url_for, render_template, request, jsonify, flash, g, session
from flask import render_template_string
from flask_login import current_user, login_required, login_user, logout_user, user_accessed

# All Trivia imports
from Trivia import app, db
from Trivia.models import DailyQusetion, Score, TrivaQuestion, User
# Utility imports
#from werkzeug import check_password_hash
import json
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
# 
from Trivia.scripts.forms import LoginForm, QuestionForm, RegisterForm, QuestionForm


@app.before_request
def before_request():
    g.user = None

    if 'Id' in session:
        user = User.query.filter_by(Id=session['Id']).first()
        g.user = user

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(form.username.data)
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        session['Id'] = user.Id
        session['marks'] = 0
        if user.last_seen.date() != datetime.today().date():
            Questions_list = TrivaQuestion().get_questions()
            for q in Questions_list:
                db.session.add(DailyQusetion(Date=datetime.today().date(), Q_id_fk=q.Question_ID,User_fk=user.Id))
                db.session.commit()
                
        
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    if g.user:
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.password = (form.password.data)
        db.session.add(user)
        db.session.commit()
        session['Id'] = user.Id
        session['marks'] = 0
        return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    form = QuestionForm()
    q_id = DailyQusetion.get_daily_qusetion(g.user.Id)
    if len(q_id) == id+1:
        db.session.add(Score(score_date=datetime.today().date(),Id_fk=g.user.Id, score= session['marks']))
        db.session.commit()
        session['marks'] = 0
        return redirect(url_for('score'))
    if not g.user:
        return redirect(url_for('login'))
    # list of questions
    q = TrivaQuestion().question(q_id[id].Q_id_fk)
    if request.method == 'POST':
        if q.check_anwser(request.form['anwser']):
            session['marks'] += 10
            
        return redirect(url_for('question', id=(id+1)))
    return render_template('question.html', form=form,  q=q, title='Question {}'.format(q.Questions), qid=id)


@app.route('/score')
def score():
    if not g.user:
        return redirect(url_for('login'))
    g.user.marks = session['marks']
    score = Score().get_score(g.user.Id).score
    high =  Score().get_today_highest()
    H_user = User().get_by_id(high.Id_fk).username
    # db.session.commit()
    return render_template('score.html', title='Final Score', high_score=high ,H_user=H_user, score=score)

@app.route('/logout')
def logout():
    if not g.user:
        return redirect(url_for('login'))
    session.pop('Id', None)
    session.pop('marks', None)
    return redirect(url_for('home'))