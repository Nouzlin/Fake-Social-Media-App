__author__ = 'linko538'
import sqlite3
from flask import g
from contextlib import closing

def connect_db(app):
    return sqlite3.connect(app.config['DATABASE'])

def get_db(app):
    db = None
    if __name__ != "__main__":
        db = getattr(g, 'db', None)
    if not db:
        db = connect_db(app)
    return db

def init(app):
    with closing(connect_db(app)) as db:
        with app.open_resource('schema.sql', mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def add_message(app, info):
    db = get_db(app)
    first_name, last_name, email, country, city, reference = info
    db.execute("insert into signups (FirstName, LastName, Email, Country, City, Reference) values (?, ?, ?, ?, ?, ?)",
               (first_name, last_name, email, country, city, reference))
    db.commit()