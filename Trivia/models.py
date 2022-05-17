# coding: utf-8

from datetime import datetime

from Trivia import db, login_manager

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash


import random

from contextlib import contextmanager


class DailyQusetion(db.Model):
    __tablename__ = 'DailyQusetion'

    Question_served = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    User_fk = db.Column(db.ForeignKey('User.Id'))
    Q_if_fk = db.Column(db.ForeignKey('TrivaQuestions.Question_ID'))

    TrivaQuestion = db.relationship(
        'TrivaQuestion', primaryjoin='DailyQusetion.Q_if_fk == TrivaQuestion.Question_ID', backref='daily_qusetions')
    User = db.relationship(
        'User', primaryjoin='DailyQusetion.User_fk == User.Id', backref='daily_qusetions')


class Score(db.Model):
    __tablename__ = 'Score'

    Score_id = db.Column(db.Integer, primary_key=True)
    Id_fk = db.Column(db.ForeignKey('User.Id'))
    score = db.Column(db.Integer)
    score_date = db.Column(db.Date)

    User = db.relationship(
        'User', primaryjoin='Score.Id_fk == User.Id', backref='scores')


class TrivaQuestion(db.Model):
    __tablename__ = 'TrivaQuestions'

    Question_ID = db.Column(db.Integer, primary_key=True)
    Questions = db.Column(db.Text, nullable=False)
    Awsers = db.Column(db.Text, nullable=False)


    
    def __rep__(self):
        return f" <ID {self.Question_ID}, Questions {self.Questions} , Awsers{self.Awsers}>"
    
    def question(self):
            return self.Questions

   
    @classmethod
    def get_questions(self, n:int= 10):
        """
        get_questions

        Return n number of question from db

        Parameters
        ----------
        n : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        
        self.last_item = self.query.order_by(self.Question_ID.desc()).first().Question_ID

        sample = random.sample(range(1, self.last_item), n)        
        
        return self.query.filter(self.Question_ID.in_(tuple(sample))).all()
       



class User(UserMixin,db.Model):
    __tablename__ = 'User'

    Id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return f'<User({self.username})>'
    
    def get_id(self):
        return (self.Id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def commits(self, user):
        db.session.add(user)
        db.session.commit()
    
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))