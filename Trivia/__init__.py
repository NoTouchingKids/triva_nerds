import csv
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

import click
from config import Config
from flask import Flask
from flask.cli import with_appcontext
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# instyal 
app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# TODO: Add centralised error handling for REST Full
# !: from Trivia.scripts import error
from Trivia import models, routes

# create command function
cwd = os.getcwd()

@click.command(name='Insert_Questions')
@with_appcontext
def Insert_Questions():
    
    Questions_list = []
    # read the  User csv that contain sample users
    with open(os.path.join(cwd, 'Sample/Trivia-Printable.csv'), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            q = models.TrivaQuestion(
                Questions=row[0],
                Anwser=row[1]
            )
            Questions_list.append(q)
            print(row)
        if app.debug:
           print(Questions_list)
        db.session.bulk_save_objects(Questions_list)
        db.session.commit()

@click.command(name="Insert_Users")
@with_appcontext
def Insert_Users():
    User_list = []
    # read the  User csv that contain sample users
    with open(os.path.join(cwd, 'Sample/User.csv'), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            u = models.User(
                username=row[0],
                email=row[1],
                about_me=row[3]
            )
            u.password = row[2]
            User_list.append(u)
        if app.debug:
           print(User_list)
        db.session.bulk_save_objects(User_list)
        db.session.commit()

@click.command(name="Insert_Score")
@with_appcontext
def Insert_Score():
    Score_list = []
    with open(os.path.join(cwd, 'Sample/Score.csv'), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            s = models.Score(
                Id_fk=row[0],
                score=row[1],
                score_date=datetime.today().date()
            )
            Score_list.append(s)
        if app.debug:
           print(Score_list)
        db.session.bulk_save_objects(Score_list)
        db.session.commit()

# add command function to cli commands
app.cli.add_command(Insert_Questions)
app.cli.add_command(Insert_Score)
app.cli.add_command(Insert_Users)


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/Trivia.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Trivia startup')
