__author__ = 'linko538'

import sqlite3
from flask import g

def connect_db(app):
    return sqlite3.connect(app.config['DATABASE'])

def close_connection(ignore_exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# If we are not connected to the DB, connect us!
def get_db(app):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db(app)
    return db

# Initialize the DB by running the sql script 'schema.sql'
def init(app):
    with app.app_context():
        db = get_db(app)
        with app.open_resource('schema.sql', mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

# Add information to the DB
def add_message(app, info):
    db = get_db(app)
    first_name, last_name, email, country, city, reference = info
    db.execute("insert into signups (FirstName, LastName, Email, Country, City, Reference) values (?, ?, ?, ?, ?, ?)",
               (first_name, last_name, email, country, city, reference))
    db.commit()

# Query number of registered users from DB
def get_signup_count(app):
    db = get_db(app)
    cursor = db.execute('select count(*) from signups')
    return cursor.fetchone()[0]

# Query information about users from DB
def get_signups(app):
    db = get_db(app)
    cursor = db.execute('select Firstname, LastName, Email, country, City, Reference from signups order by ID desc')
    signups = [dict(name=row[0] + " " + row[1], email=row[2], country=row[3], city=row[4], reference=row[5])
               for row in cursor.fetchall()]
    return signups
