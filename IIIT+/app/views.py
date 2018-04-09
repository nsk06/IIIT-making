from flask import *
from flask_bootstrap import Bootstrap
from Key import Config
from login import Login
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import *
from database import User
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from database import 
login = LoginManager(app)
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nonidh'}
    posts = [
        {
            'author': {'username': 'Pratyush'},
            'body': 'Hello peeps!'
        },
        {
            'author': {'username': 'Harshit'},
            'body': 'Project pura kro bhaiya!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
@app.route('/login',methods  = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
if __name__ == '__main__':
    app.debug = True
    app.run()
