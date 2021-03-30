# Don't call this flask.py!
# Documentation for Flask can be found at:
# https://flask.palletsprojects.com/en/1.1.x/quickstart/

from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os 
from pathlib import Path

app = Flask(__name__)
app.secret_key = b'REPLACE_ME_x#pi*CO0@^z'

sqlite_uri = 'sqlite:///' + os.path.abspath(os.path.curdir) + '/meowzers.db'
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Profile

IMAGE_DIR = 'static/img/profilephotos'



@app.before_first_request
def app_startup():
    imgdir = Path(IMAGE_DIR)
    if not imgdir.exists():
        imgdir.mkdir(parents=True)
    try:
        Profile.query.all()
    except:
        db.create_all()
        if 'username' in session:
            del session['username']



@app.before_request
def login_check():
    securedUrls = ['/', '/main/', '/logout/']
    if 'username' not in session and request.path in securedUrls:
        return redirect(url_for('login'))



@app.route('/')
def index():
    return redirect(url_for('main'))
    


@app.route('/main/', methods=['GET'])
def main():
    return 'Welcome {}!'.format(session['username'])



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # check if fields are not empty, else display error message
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            errMsg = 'One or more fields was left empty'
            return render_template('login.html', message=errMsg)

        # check if username is registered, if not display error message
        if db.session.query(Profile.id).filter_by(username=username).first() is None:
            errMsg = 'Username is not registered with an account'
            return render_template('login.html', message=errMsg)
     
        # if username is registered, check if password matched. If it does
        # save username in session and redirect to main, else produce error message      
        if db.session.query(Profile.password).filter_by(username=username).first()[0] != password:
            errMsg = 'Incorrect password'
            return render_template('login.html', message=errMsg)
        
        session['username'] = username
        return redirect(url_for('main'))



@app.route('/logout/', methods=['GET'])
def logout():
    del session['username']
    return redirect(url_for('login'))



@app.route('/profile/create/', methods=['GET'])
def profile_create():
    return render_template('profile_create.html')



@app.route('/profile/', methods=['POST'])
def profile():
    # set form data to variables
    username = request.form['username']
    password = request.form['password']
    email = request.form ['email']
    infile = request.files['profilePic']
    
    # check if any fields were empty if so produce error message
    if username == '' or password == '' or email == '':
        errMsg = 'One or more fields was left empty'
        return render_template('profile_create.html', message=errMsg)

    # check if user name already exists if so produce error message
    if db.session.query(Profile.id).filter_by(username=username).first() is not None:
        errMsg = 'That username is already taken'
        return render_template('profile_create.html', message=errMsg)
    
    # check if a file was selected, if so, all criteria are met
    # and profile is created
    if infile:
        filename = username+'.jpg'
        filepath = os.path.join(IMAGE_DIR, filename)
        infile.save(filepath)
        profile = Profile(username=username, password=password, email=email, photofn=filename)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('login'))

    # If  file is not selected produce error message    
    else:
        errMsg = 'Must include a profile picture'
        return render_template('profile_create.html', message=errMsg)
