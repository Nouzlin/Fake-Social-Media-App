__author__ = 'Linus'
from flask import Flask, flash, render_template, request, g
import database, sqlite3

# configuration
DATABASE = 'app_db.db'

app = Flask(__name__)
app.secret_key ="PEPPARKAKS_bagare_IN_da_HOUSE"
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/new_signup", methods=['POST'])
def new_signup():
    info = [request.form['firstName'], request.form['lastName'], request.form['email'],
            request.form['country'], request.form['city'], request.form['reference']]

    try:
        database.add_message(app, info)
        signups_count = database.get_signup_count(app)
        return render_template('register_completed.html', signups=signups_count)
    except sqlite3.IntegrityError:
        flash('Email already signed up')
        return signup()

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

if __name__ == "__main__":
    #database.init(app)
    app.run(host="localhost", debug=True)
