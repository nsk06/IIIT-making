from views import db,login
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from passlib.context import CryptContext
from flask_login import UserMixin
#from login import Login
pwd_context = CryptContext(

    schemes=["pbkdf2_sha512"],
    default="pbkdf2_sha512",
    all__vary_rounds = 0.2,
    pbkdf2_sha512__default_rounds = 8000,
    )
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password,self.password_hash)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)