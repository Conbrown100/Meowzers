# Don't call this flask.py!
# Documentation for Flask can be found at:
# https://flask.palletsprojects.com/en/1.1.x/quickstart/

from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
app.secret_key = b'REPLACE_ME_x#pi*CO0@^z'

sqlite_uri = 'sqlite:///' + os.path.abspath(os.path.curdir) + '/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Profile

@app.route('/')
def index():
    return redirect(url_for('main'))
    
@app.route('/main/', methods=['GET'])
def main():
    return 'Here is your main page'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return 'Not yet implemented'

@app.route('/logout/', methods=['GET'])
def logout():
    return 'Not yet implemented'

@app.route('/profile/create/', methods=['GET'])
def profile_create():
    return 'Not yet implemented'

@app.route('/profile/', methods=['POST'])
def profile():
    return 'Not yet implemented'

