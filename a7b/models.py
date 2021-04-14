
from appserver import db                                                        

# FIXME add serialize() method to all model classes.

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(144), unique=False, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    likes = db.relationship('Like', backref='post', uselist=True, lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'profile': self.profile.serialize(),
            'numLikes': len(self.likes),
        }

    def __repr__(self):
        return '<Post id=%r>' % self.id

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(16), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    photofn = db.Column(db.String(80), unique=False, nullable=True)
    posts = db.relationship('Post', backref='profile', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'photofn': self.photofn,
        }

    def __repr__(self):
        return '<Profile id=%r>' % self.id

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    profile = db.relationship('Profile', uselist=False, lazy=True)
    # This doesn't work because a post does not have a single like.
    # The post likes relationship was already defined in Post.
    #post = db.relationship('Post', uselist=False, lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'post': self.post.serialize(),
            'profile': self.profile.serialize(),
        }

    def __repr__(self):
        return '<Like id=%r>' % self.id
