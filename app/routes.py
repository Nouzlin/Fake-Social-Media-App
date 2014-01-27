__author__ = 'Linus'
from flask import Flask, render_template, request
import database

# configuration
DATABASE = 'app_db.db'

app = Flask(__name__)
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
    database.add_message(app, info)
    return render_template('register_completed.html')

if __name__ == "__main__":
    #database.init(app)
    app.run(debug=True)
