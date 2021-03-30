# Don't call this flask.py!
# Documentation for Flask can be found at:
# https://flask.palletsprojects.com/en/1.1.x/quickstart/

from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os 

app = Flask(__name__)
app.secret_key = b'REPLACE_ME_x#pi*CO0@^z'

sqlite_uri = 'sqlite:///' + os.path.abspath(os.path.curdir) + '/app.db'
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
    return render_template('profile_create.html')

@app.route('/profile/', methods=['POST'])
def profile():
    username = request.form['username']
    password = request.form['password']
    email = request.form ['email']
    infile = request.files['profilePic']

    if username == '' or password == '' or email == '':
        return render_template('profile_create.html', message='One or more fields was left empty')

    if db.session.query(Profile.id).filter_by(username=username).first() is not None:
        return render_template('profile_create.html', message='That username is already taken')

    if infile:
        #filename = secure_filename(infile.filename)
        filename = username+'.jpg'
        filepath = os.path.join(IMAGE_DIR, filename)
        infile.save(filepath)
        profile = Profile(username=username, password=password, email=email, photofn=filename)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('login'))
    
    else:
        return render_template('profile_create.html', message='Must include a profile picture')
