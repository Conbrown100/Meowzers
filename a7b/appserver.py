# Don't call this flask.py!
# Documentation for Flask can be found at:
# https://flask.palletsprojects.com/en/1.1.x/quickstart/

from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort
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

from models import Profile, Post, Like

IMAGE_DIR = 'static/img/profilephotos'


def get_current_profile():
    if 'id' in session:
        return Profile.query.get(session['id'])

    return None


def is_secure_path(request):
    return request.path not in [
                '/profile/',
                '/profile/create/',
                '/login/',
                '/api/docs/',
            ] and not request.path.startswith('/static/')


@app.before_first_request
def app_startup():
    imgdir = Path(IMAGE_DIR)
    if not imgdir.exists():
        imgdir.mkdir(parents=True)
    try:
        Profile.query.all()
    except:
        db.create_all()
        if 'id' in session:
            del session['id']


@app.before_request
def login_check():
    if 'id' not in session and is_secure_path(request):
        return redirect(url_for('login_form'))


@app.route('/')
def index():
    return redirect(url_for('main'))    


@app.route('/main/', methods=['GET'])
def main():
    return render_template('main.html', profile=get_current_profile())


@app.route('/login/', methods=['GET'])
def login_form():
    if request.method == 'GET':
        return render_template('login.html')
        
        
@app.route('/login/', methods=['POST'])
def login():
    profile = Profile.query.filter_by(username=request.form['username']).first()

    if profile and profile.password == request.form['password']:
        session['id'] = profile.id
        return redirect(url_for('main'))

    errMsgs = ['Invalid username/password combination']
    return render_template(
            'login.html',
            messages=errMsgs)


@app.route('/logout/', methods=['GET'])
def logout():
    del session['id']
    return redirect(url_for('login_form'))


@app.route('/profile/create/', methods=['GET'])
def profile_form():
    return render_template('profile_create.html')


@app.route('/profile/', methods=['POST'])
def create_profile():
    # set form data to variables
    username = request.form['username']
    password = request.form['password']
    email = request.form ['email']
    photoFile = request.files['profilePic']
    
    # check if any fields were empty if so produce error message
    if username == '' or password == '' or email == '':
        errMsgs = ['One or more fields was left empty']
        return render_template('profile_create.html', messages=errMsgs)

    # check if user name already exists if so produce error message
    if db.session.query(Profile.id).filter_by(username=username).first() is not None:
        errMsgs = ['That username is already taken']
        return render_template('profile_create.html', messages=errMsgs)
    
    # check if a file was selected, if so, all criteria are met
    # and profile is created
    if photoFile:
        filename = username+'.jpg'
        filepath = os.path.join(IMAGE_DIR, filename)
        photoFile.save(filepath)

        profile = Profile(username=username, password=password, email=email, photofn=filename)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('login_form'))

    # If  file is not selected produce error message    
    else:
        errMsgs = ['Must include a profile picture']
        return render_template('profile_create.html', messages=errMsgs)


@app.route('/profile/', methods=['GET'])
def my_profile():
    if get_current_profile() != None:
        return render_template('profile.html', profile=get_current_profile())
    return redirect(url_for('login_form'))


@app.route('/profile/<int:profile_id>/', methods=['GET'])
def show_profile(profile_id):
    other_profile = Profile.query.get(profile_id)
    if other_profile:
        return render_template('profile.html', profile=other_profile)
    else:
        abort(404)


# ---- REST Endpoints below here ----


@app.route('/api/posts/', methods=['GET'])
def api_get_posts():
    '''
      Params:
        profile_id : integer (optional) - a specific user ID
        if omitted, only gets current user's posts

      Returns:
        A JSON array of Profile objects. If the profile_id is invalid
        this returns [].
    '''
    profile_id = get_current_profile().id
    if 'profile_id' in request.args:
        profile_id = request.args.get('profile_id')

    posts = Post.query.filter_by(profile_id=profile_id).all()
    posts = list(map(lambda post: post.serialize(), posts))
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>/', methods=['GET'])
def api_get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify(post.serialize())
    else:
        abort(404)


@app.route('/api/posts/', methods=['POST'])
def api_post_posts():
    '''
      Params:
        content : string (required)

      Returns:
        A JSON Post object
    '''
    post = Post(content=request.form['content'], profile=get_current_profile())
    db.session.add(post)
    db.session.commit()
    print('Created new post with id = %d and profile_id = %d' % (post.id, post. profile.id))
    return jsonify(post.serialize())


@app.route('/api/posts/<int:post_id>/like/', methods=['POST'])
def api_posts_like(post_id):
    profile = get_current_profile()
    post = Post.query.get(post_id)
    if post:
        # Only get to like if I haven't already.
        my_likes = list(filter(lambda likey: likey.profile.id == profile.id,    post.likes))
        if len(my_likes) == 0:
            db.session.add(Like(profile=profile, post=post))
            db.session.commit()
        return jsonify(post.serialize())
    else:
        abort(404)


@app.route('/api/posts/<int:post_id>/unlike/', methods=['POST'])
def api_posts_unlike(post_id):
    profile = get_current_profile()
    post = Post.query.get(post_id)
    # Can only unlike if I have previously liked.
    likey = Like.query.filter(and_(Like.post==post, Like.profile==profile)).    first()
    if likey:
        db.session.delete(likey)
        db.session.commit()
        return jsonify(post.serialize())
    elif not post:
        abort(404)
    else:
        return jsonify(post.serialize())


@app.route('/api/posts/<int:post_id>/likes/', methods=['GET'])
def api_posts_numlikes(post_id):
    post = Post.query.get(post_id)
    if post:
        likes = Like.query.filter_by(post=post).all()
        profiles = list(map(lambda likey: likey.profile.serialize(), likes))
        return jsonify(profiles)
    else:
        abort(404)


@app.route('/api/docs/', methods=['GET'])
def api_docs():
    return render_template('docs.html')

