__author__ = 'linko538'
import sqlite3
from flask import g

def connect_db(app):
    return sqlite3.connect(app.config['DATABASE'])

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_db(app):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db(app)
    return db

def init(app):
    with app.app_context():
        db = get_db(app)
        with app.open_resource('schema.sql', mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def add_message(app, info):
    db = get_db(app)
    first_name, last_name, email, country, city, reference = info
    db.execute("insert into signups (FirstName, LastName, Email, Country, City, Reference) values (?, ?, ?, ?, ?, ?)",
               (first_name, last_name, email, country, city, reference))
    db.commit()

def get_signup_count(app):
    db = get_db(app)
    cursor = db.execute('select count(*) from signups')
    return cursor.fetchone()[0]

def get_signups(app):
    db = get_db(app)
    cursor = db.execute('select * from signups')
    return cursor.fetchall()
