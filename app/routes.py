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

# Home page of the website
@app.route('/')
def home():
    return render_template('home.html')

# About-page mapping
# Shows all the tweets, so we better get them!
@app.route('/about')
def about():
    tweets = social.get_tweets('#TDDD80')
    return render_template('about.html', tweets=tweets)

# Sign up page mapping
@app.route('/signup')
def signup(data=list()):
    return render_template('signup.html', data=data)

# Get given information and post it to the DB
@app.route("/new_signup", methods=['POST'])
def new_signup():
    info = [request.form['first_name'], request.form['last_name'], request.form['email'],
            request.form['country'], request.form['city'], request.form['reference']]

    try:
        # Add the message, throws sqlite3.IntegrityError
        database.add_message(app, info)

        # Get the number of people signed up
        signups_count = database.get_signup_count(app)

        # Tweet that we have a new recruit!
        social.tweet(info)

        # Visualize for the user that everything went O.K.
        return render_template('register_completed.html', signups=signups_count)

    except sqlite3.IntegrityError:
        # Show a message describing the error for the user
        flash('Email already signed up')
        return signup(info)

# Login page mapping
# Checks if the entered password and username is correct
# Enables some new features
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

# Share story page mapping
# Retrieves and hands over the oauth token
# to the 'share_story' function in 'social.py'
@app.route('/share_story')
def share_story():
    oauth_token = request.cookies.get("oauth_token")
    social.share_story(oath_token=oauth_token)
    return render_template('story_completed.html')

# Web-page only available to admins.
# Lists information about signed up users.
@app.route('/show_signups')
def show_signups():
    try:
        # Check if we are logged in this session.
        if not session['logged_in']:
            Flask.abort(401)
        return render_template('show_signups.html', signups=database.get_signups(app))
    except KeyError:
        # Visualize for the user that something went wrong.
        flash('You need to be logged in to view that page')
        return redirect(url_for('home'))

# Do some resource deallocation
@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

if __name__ == "__main__":
    # Reset DB?
    #database.init(app)

    app.run()
