# Project Trivia quiz

<div id="top"></div>

<br />
<div align="center">
  <a href="https://github.com/NoTouchingKids/triva_nerds/blob/ff4947e04ffa7bdb7f568eca5985707805d74fdf/Reasource/Home Page.png">
    <img src="images/logo.png" alt="Logo">
  </a>

  <h3 align="center">Trivia</h3>

  <p align="center">
    Group Projet For CITS 3403
    <br />
    <a href="https://github.com/github_username/Trivia"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/github_username/Trivia/issues">Report Bug</a>
    <a href="https://github.com/github_username/Trivia/issues">Request Feature</a>
  </p>
</div>



<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



## About The Project

This was a group project assigned to student of CTIS 3401.
The Idea was to create a web site that dynamic assigned the user with set of Trivia question which the user was supposed to anwser.
The applaction trak user's progress and assign a socre depanting on how the user has performed. 
And the score is displayed on the leaderboard and allow user to compaire themself againt other.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [flask](https://flask.palletsprojects.com/en/2.1.x/)

<p align="right">(<a href="#top">back to top</a>)</p>



## Getting Started

Download the repository. then create a python viurtual enviroment and install dependency.

### Some usefull commands for admin 
* For adding Trivia question to database
   ```sh
   flask Insert_Questions
   ```
* For adding smaple score to database
   ```sh
   flask Insert_Score
   ```
* For adding sample user to database
   ```sh
   flask Insert_Users
   ```



### Prerequisites
This are all included reqiment.txt

* alembic==1.7.7
* autopep8==1.6.0
* bcrypt==3.2.2
* cffi==1.15.0
* click==8.1.3
* dnspython==2.2.1
* email-validator==1.2.1
* Flask==2.1.2
* Flask-Bcrypt==1.0.1
* Flask-HTTPAuth==4.6.0
* Flask-Login==0.6.1
* Flask-Migrate==3.1.0
* Flask-SQLAlchemy==2.5.1
* Flask-WTF==1.0.1
* greenlet==1.1.2
* idna==3.3
* importlib-metadata==4.11.3
* importlib-resources==5.7.1
* install==1.3.5
* itsdangerous==2.1.2
* Jinja2==3.1.2
* Mako==1.2.0
* MarkupSafe==2.1.1
* pycodestyle==2.8.0
* pycparser==2.21
* python-dotenv==0.20.0
* SQLAlchemy==1.4.36
* toml==0.10.2
* Werkzeug==2.1.2
* WTForms==3.0.1
* zipp==3.8.0


### Installation

1. get python 3.8 or equalent (flask is most stable on 3.8)

2. Clone the repo
   ```sh
   git clone https://github.com/NoTouchingKids/triva_nerds.git
   ```
3. Create enviroment
   ```sh
   python -m venv
   ```
4. Activate the enviroment
   ```sh
   source venv/bin/activate
   ```
5. Activate the enviroment
   ```sh
   pip install -r requirements.txt
   ```
6. add some question to database before
   ```sh
   flask Insert_Questions
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


## Usage

1. run flask for bash
   ```sh
   cd triva_nerds/
   ```

2. run flask for bash
   ```sh
   export FLASK_APP=app
   flask run
   ```

2. run flask for windows
   ```sh
   set FLASK_APP=app
   flask run
   ```

3. Go to the localhost url on port 5000
   ```sh
   Running on http://127.0.0.1:5000
   ```
   
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Add Sample data
- [x] Add Admin command 
- [ ] Add REST authantication
- [ ] Add REST json responce handling for questions
- [ ] Fix data dupication on user fail to register

<p align="right">(<a href="#top">back to top</a>)</p>