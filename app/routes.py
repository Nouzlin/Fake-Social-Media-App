from flask.ext.mail import Mail

__author__ = 'Linus'
from flask import (Flask, flash, render_template, session, redirect,
                   url_for, request, jsonify, abort, make_response)

from flask_shorturl import ShortUrl
import database
import sqlite3
import os
import social
import mail_service
import cipher

# configuration
DATABASE = 'app_db.db'
SECRET_KEY = os.urandom(128)
USERNAME = 'admin'
PASSWORD = 'MySuper1337Password'
HOST = 'localhost'

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'linus.kortesalmi@gmail.com'
MAIL_PASSWORD = 'pass'

# administrator list
ADMINS = ['linus.kortesalmi@gmail.com']



app = Flask(__name__)
app.config.from_object(__name__)
mail = Mail(app)
su = ShortUrl(app)

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
        database.add_registered_user(info)

        # Get the number of people signed up
        signups_count = database.get_signup_count()

        # Tweet that we have a new recruit!
        #social.tweet(info)

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
            abort(401)
        return render_template('show_signups.html', signups=database.get_signups())
    except KeyError:
        # Visualize for the user that something went wrong.
        flash('You need to be logged in to view that page')
        return redirect(url_for('home'))

# Create group page
@app.route("/create_group")
def create_group():
    try:
        # Check if we are logged in this session.
        if not session['logged_in']:
            abort(401)
        return render_template('create_group.html', signups=database.get_persons_and_ids())
    except KeyError:
        # Visualize for the user that something went wrong.
        flash('You need to be logged in to view that page')
        return redirect(url_for('home'))

@app.route('/show_groups', methods=['GET'])
def show_groups():
    try:
        # Check if we are logged in this session.
        if not session['logged_in']:
            abort(401)

        group_list = database.get_groups()
        group_member_lists = dict()  # Create a dictionary with (key, value) being (group_name, members)
        for group in group_list:
            # For each group: add a list of its members
            group_member_lists[group['name']] = database.get_group_members(group['name'])
        return render_template('show_groups.html', groups=group_list, member_lists=group_member_lists)

    except KeyError:
        # Visualize for the user that something went wrong.
        flash('You need to be logged in to view that page')
        return redirect(url_for('home'))

@app.route('/new_group', methods=['POST'])
def new_group():
    try:
        # Check if we are logged in this session.
        if not session['logged_in']:
            abort(401)

        group_name = request.form['group_name']
        priority = request.form['priority']
        database.create_new_group(group_name, priority)
        database.add_group_members(group_name, request.form.getlist('person_id'))

        flash('Group created')
        return redirect(url_for('create_group'))

    except KeyError:
        # Visualize for the user that something went wrong.
        flash('You need to be logged in to view that page')
        return redirect(url_for('home'))

    except sqlite3.IntegrityError:
        flash('Group already exists')
        return redirect(url_for('create_group'))

@app.route('/email_group/<string:group_id>')
def email_group(group_id):
    try:
        # Check if we are logged in this session.
        if not session['logged_in']:
            abort(401)

        group_name = database.get_group(group_id)['name']
        members = database.get_group_members(group_name)
        mail_service.send_information_email(group_id, members)
        flash('Email sent')
        return show_groups()

    except KeyError:
        # Visualize for the user that something went wrong.
        flash('You need to be logged in to view that page')
        return redirect(url_for('home'))

@app.route('/user/<string:coded_info>')
def click_tracker(coded_info):
    decoded_info = cipher.decrypt_val(coded_info)
    group_id = decoded_info['group_id']
    person_id = decoded_info['person_id']

    database.set_email_clicked(group_id, person_id)
    return redirect(url_for('home'))


###############################################################################
# REST FUNCTIONS ##############################################################
###############################################################################
# Web-page only available to admins.
# Lists all created groups
@app.route('/api/v1.0/groups', methods=['GET'])
def handle_groups():
    groups = jsonify({'groups': database.get_groups()})
    return groups, 200

@app.route('/api/v1.0/groups/<string:group_name>', methods=['GET'])
def get_group_members(group_name):
    members = database.get_group_members(group_name)
    return jsonify({'members': members})

###############################################################################
# Clean up and Error handling #################################################
###############################################################################
# Do some resource deallocation
@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

if __name__ == "__main__":
    # Reset DB?
    if not os.path.isfile(DATABASE):
        database.init(app)

    app.run(debug=True)

