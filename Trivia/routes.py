from datetime import datetime
from flask import g, redirect, render_template, request, session, url_for
from werkzeug.urls import url_parse

# All Trivia imports
from Trivia import app, db
from Trivia.models import DailyQusetion, Score, TrivaQuestion, User
from Trivia.scripts.forms import LoginForm, QuestionForm, RegisterForm




@app.before_request
def before_request():
    # current user session to none.
    g.user = None
    # get user object from database.
    if 'Id' in session:
        user = User.query.filter_by(Id=session['Id']).first()
        g.user = user


@app.route('/')
def home():
    # render the home page.
    # get the leaderboard from the database.
    return render_template('index.html', title='Home', leaderborad=Score.get_top())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # check if the form fied are field out correctly.
    if form.validate_on_submit():
        # get user instance.
        user = User.get_user(form.username.data)
        # check user password.
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        # inistalise user session.
        session['Id'] = user.Id
        session['marks'] = 0
        # assign new question to user if not being assigned any.
        if user.last_seen.date() != datetime.today().date():
            Questions_list = TrivaQuestion().get_questions()
            for q in Questions_list:
                db.session.add(DailyQusetion(Date=datetime.today(
                ).date(), Q_id_fk=q.Question_ID, User_fk=user.Id))
                db.session.commit()
        # rediect to home page with user session.
        # TODO: expermenting with a different style of redict.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    # check if user is none
    if g.user:
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
     # check if the form fied are field out correctly
    if form.validate_on_submit():
        # create nerw user object 
        user = User(username=form.username.data, email=form.email.data)
        # !:    Im using the setter method so sign the password.
        # !:    yes I could directly call hash password but not secure.
        # set password set as hash
        user.password = (form.password.data)
        # user to database 
        db.session.add(user)
        db.session.commit()
        # inistalise user session
        session['Id'] = user.Id
        session['marks'] = 0
        # assign new question to user if not being assigned any.
        # TODO: need work to make sure that it does not duplicate entry.
        Questions_list = TrivaQuestion().get_questions()
        for q in Questions_list:
            db.session.add(DailyQusetion(Date=datetime.today(
            ).date(), Q_id_fk=q.Question_ID, User_fk=user.Id))
            db.session.commit()
        # rediect to home page with user session.
        return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# TODO: this module needs a rewrite as it will break
@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    # check if user is none.
    if not g.user:
        return redirect(url_for('login'))
    # TODO: this will be remove when this app is updated to use REST.
    id = id-1
    form = QuestionForm()
    # get list of Question assigned to user.
    q_id = DailyQusetion.get_daily_qusetion(g.user.Id)
    # check for end of the question list.
    if len(q_id) == id:
        # 
        db.session.add(Score(score_date=datetime.today().date(),
                       Id_fk=g.user.Id, score=session['marks']))
        db.session.commit()
        #if 
        return redirect(url_for('score'))
   
    # list of questions.
    q = TrivaQuestion().question(q_id[id].Q_id_fk)
    # check for anwser POST request.
    if request.method == 'POST':
        # check anwser is correct of not.
        if q.check_anwser(request.form['anwser']):
            # add ten point for correct answer. 
            session['marks'] += 10
        return redirect(url_for('question', id=(id+2)))
    return render_template('question.html', form=form,  q=q, title='Question {}'.format(q.Questions), qid=id+1)


@app.route('/score')
def score():
    # check if user is none.
    if not g.user:
        return redirect(url_for('login'))
    
    # get current user high score.
    current_user_socre = session['marks']
    # get user best score.
    user_best = Score().get_score(g.user.Id).score
    # that day's high score.
    high = Score().get_today_highest()
    # user of that day's high score.
    H_user = User().get_by_id(high.Id_fk).username
    # rest the score to 0
    session['marks'] = 0
    
    return render_template('score.html', user_best=user_best, high_today=high, H_user=H_user, score=current_user_socre,
                            leaderborad=Score.get_top()
                           )


@app.route('/logout')

def logout():
    # check if user is none.
    if not g.user:
        return redirect(url_for('login'))
    # remove user session
    session.pop('Id', None)
    session.pop('marks', None)
    return redirect(url_for('home'))
