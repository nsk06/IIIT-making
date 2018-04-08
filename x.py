from flask import *
from flask_bootstrap import Bootstrap
from Key import Config
from login import Login
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
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
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
@app.route('/login',methods  = ['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
if __name__ == '__main__':
    app.debug = True
    app.run()