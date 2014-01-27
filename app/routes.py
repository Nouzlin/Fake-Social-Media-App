__author__ = 'Linus'
from flask import Flask, render_template, request, g
#import message_adt
#import my_db

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/register_complete", methods=['POST'])
def send_interest():
    email = request.form['email']
    #my_db.add_message(email)
    return render_template('register_complete.html')

if __name__ == "__main__":
    app.run(debug=True)