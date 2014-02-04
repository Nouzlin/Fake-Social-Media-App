__author__ = 'Linus'
from flask import Flask, flash, render_template, session, redirect, url_for, request, g
import database, sqlite3, os, social

# configuration
DATABASE = 'app_db.db'
DEBUG = True
SECRET_KEY = os.urandom(128)
USERNAME = 'admin'
PASSWORD = 'MySuper1337Password'
HOST = 'localhost'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup(data=list()):
    if not data:
        return render_template('signup.html')
    return render_template('signup_try_again.html')

@app.route("/new_signup", methods=['POST'])
def new_signup():
    info = [request.form['first_name'], request.form['last_name'], request.form['email'],
            request.form['country'], request.form['city'], request.form['reference']]

    try:
        database.add_message(app, info)
        signups_count = database.get_signup_count(app)
        return render_template('register_completed.html', signups=signups_count)
    except sqlite3.IntegrityError:
        flash('Email already signed up')
        return signup(info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (request.form['username'] != app.config['USERNAME'] or
            request.form['password'] != app.config['PASSWORD']):
            flash('Invalid username or password')
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_signups'))
    return render_template('login.html')

@app.route('/register_completed')
def register_completed():
    #oauth_token = request.cookies.get("oauth_token")
    #social.upload_wall(oath_token=oauth_token)
    return render_template('register_completed.html')

@app.route('/show_signups')
def show_signups():
    try:
        if not session['logged_in']:
            Flask.abort(401)
        return render_template('show_signups.html', signups=database.get_signups(app))
    except KeyError:
        flash('You need to be logged in to view that page')
        return redirect(url_for('home'))

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

if __name__ == "__main__":
    #database.init(app)
    app.run()
