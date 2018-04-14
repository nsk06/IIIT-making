from views import db,log
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

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
group = db.Table('Groups',
    db.Column('userid',db.Integer,db.ForeignKey('user.id')),
    db.Column('groupname',db.String(64),index=True,unique=True))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password,self.password_hash)
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


@log.user_loader
def load_user(id):
    return User.query.get(int(id))
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Group(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id'))
    groupname = db.Column(db.String(64),index=True)
    adminId =  db.Column(db.Integer)
    members = db.relationship(
        'User', secondary=group,
        primaryjoin=(group.c.userid == id),
        secondaryjoin=(group.c.groupname == id),
        backref=db.backref('Group', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Group {}>'.format(self.groupname)
    def addMember(self,user):
        if not self.is_member(user):
            self.members.append(user)
    def is_member(self, user):
        return self.members.filter(
            group.c.self.userid == user.id).count() > 0                                     
    def removeMember(self,user):
        if self.is_member(user):
            self.members.remove(user)
    def grouppost(self):
        gname=self.groupname
        groupusers = Group.query.filter(Group.groupname == gname).all()
        #groupusers = groupusers.items
        #print(groupusers)
        for mem in groupusers:
            groupposts = Post.query.filter(mem.userid == Post.user_id)
        return groupposts.order_by(Post.timestamp.desc())
