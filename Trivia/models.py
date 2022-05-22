# coding: utf-8

from datetime import datetime
from sqlalchemy import func, and_
from Trivia import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import random


class DailyQusetion(db.Model):
    __tablename__ = 'DailyQusetion'

    Question_served = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    User_fk = db.Column(db.ForeignKey('User.Id'))
    Q_id_fk = db.Column(db.ForeignKey('TrivaQuestions.Question_ID'))

    TrivaQuestion = db.relationship(
        'TrivaQuestion', primaryjoin='DailyQusetion.Q_id_fk == TrivaQuestion.Question_ID', backref='daily_qusetions')
    User = db.relationship(
        'User', primaryjoin='DailyQusetion.User_fk == User.Id', backref='daily_qusetions')

    @classmethod
    def get_daily_qusetion(self, user_id):
        """
        get_daily_qusetion : get the Question that are assigned to user when logined

        Parameters
        ----------
        user_id : Int
            User Id

        Returns
        -------
        DailyQusetion
            return list of 10 qestion that assigned to user
        """
        return self.query.filter_by(Date=datetime.today().date(), User_fk=user_id).limit(10).all()


class Score(db.Model):
    """
    Score : This object stores the score of each game the user plays
    """
    __tablename__ = 'Score'

    Score_id = db.Column(db.Integer, primary_key=True)
    Id_fk = db.Column(db.ForeignKey('User.Id'))
    score = db.Column(db.Integer)
    score_date = db.Column(db.Date)

    # relationship with user table
    User = db.relationship(
        'User', primaryjoin='Score.Id_fk == User.Id', backref='scores')

    def get_score(self, user_id):
        """
        get_score : get score for curent user

        Parameters
        ----------
        user_id : int
            User Id from user table / instance

        Returns
        -------
        Socre
            Return the score object 
        """
        return self.query.filter_by(score_date=datetime.today().date(), Id_fk=user_id).first()

    @classmethod
    def get_today_highest(self):
        """
        get_today_highest : Return the hight score of the day

        Returns
        -------
        Socre
            Return the hight score object of the day
        """
        return self.query.filter_by(score_date=datetime.today().date()).first()

    @classmethod
    def get_top(self) -> list:
        """
        get_top : Get top 10 user and their score for that day.

        Returns
        -------
        leaderborad
            list of tupbe in order of person thie hightest score to lowerest.
        """
        leaderborad = db.session.query(
            User.username,
            func.max(Score.score)
        ).join(Score).group_by(Score.Id_fk).order_by(Score.score.desc()).limit(20).all()
        return leaderborad


class TrivaQuestion(db.Model):
    __tablename__ = 'TrivaQuestions'

    Question_ID = db.Column(db.Integer, primary_key=True)
    Questions = db.Column(db.Text, nullable=False)
    Anwser = db.Column(db.Text, nullable=False)

    def __rep__(self):
        return f" <ID {self.Question_ID}, Questions {self.Questions} , Awsers{self.Awsers}>"

    def question(self, id):
        return self.query.filter_by(Question_ID=id).first()

    @classmethod
    def get_questions(self, n: int = 10):
        """
        get_questions : get question from Table

        Parameters
        ----------
        n : int, optional
            number of question that queryed, by default 10

        Returns
        -------
        TrivaQuestion
            List of TrivaQuestion object 
        """
        self.last_item = self.query.order_by(
            self.Question_ID.desc()).first().Question_ID
        # get a list size 10 where the upper bond is last row id from TrivaQuestion table
        sample = random.sample(range(1, self.last_item), n)
        # take the list convert it to tuple and query the TrivaQuestion table
        # for index that match the question id
        return self.query.filter(self.Question_ID.in_(tuple(sample))).all()

    def check_anwser(self, anwser):
        """
        check_anwser : Check if anwser correct or not
        
        Parameters
        ----------
        anwser : string
            this from user intput

        Returns
        -------
        bool
            if correct then true
        """
        if anwser is None or anwser == "":
            return False
        if self.Anwser.lower() == anwser.lower():
            return True
        else:
            return False


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    Id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    marks = db.Column(db.Integer, index=True, default=0)

    def __repr__(self):
        return f'<User({self.username})>'

    def get_by_id(self, id):
        return self.query.filter_by(Id=id).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user(self, username):
        return self.query.filter_by(username=username).first()

# user session initaliser
@login_manager.user_loader
def load_user(Id):
    return User.query.get(int(Id))
