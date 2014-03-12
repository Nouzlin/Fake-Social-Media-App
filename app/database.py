__author__ = 'linko538'

import sqlite3
import re
from flask import g
import routes


def connect_db():
    return sqlite3.connect(routes.app.config['DATABASE'])

def close_connection(ignore_exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# If we are not connected to the DB, connect us!
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

# Initialize the DB by running the sql script 'schema.sql'
def init(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

# Add information to the DB
def add_registered_user(info):
    db = get_db()
    first_name, last_name, email, country, city, reference = info
    db.execute('INSERT INTO signups (FirstName, LastName, Email, Country, City, Reference) VALUES (?, ?, ?, ?, ?, ?)',
               (first_name, last_name, email, country, city, reference))
    db.commit()

# Query number of registered users from DB
def get_signup_count():
    db = get_db()
    cursor = db.execute('select count(*) from signups')
    return cursor.fetchone()[0]

# Query information about users from DB
def get_signups():
    db = get_db()
    cursor = db.execute('SELECT FirstName, LastName, Email, Country, City, Reference FROM signups ORDER BY Id DESC')
    signups = [dict(name=row[0] + " " + row[1], email=row[2], country=row[3], city=row[4], reference=row[5])
               for row in cursor.fetchall()]
    return signups

def get_persons_and_ids():
    db = get_db()
    cursor = db.execute('SELECT FirstName, LastName, ID FROM signups ORDER BY Id DESC')
    persons_and_ids = [dict(name=row[0] + " " + row[1], id=row[2]) for row in cursor.fetchall()]
    return persons_and_ids

def is_allowed_name(table_name):
    # Does the table name only consist of alphanumeric characters?
    return re.match('^[\w-]+$', table_name, flags=re.UNICODE) is not None

def create_new_group(group_name, priority):
    if not is_allowed_name(group_name):
        raise SyntaxError(group_name + " is not an allowed group name")

    db = get_db()
    db.execute('INSERT INTO groups (Name, Priority) VALUES (?, ?)', (group_name, priority))
    db.execute('CREATE TABLE ' + group_name + ' (Id INT PRIMARY KEY NOT NULL UNIQUE, Answered BOOLEAN DEFAULT FALSE)')
    db.commit()


def add_group_members(group_name, members):
    if not is_allowed_name(group_name):
        raise SyntaxError(group_name + " is not an allowed group name")

    db = get_db()
    for member_id in members:
        db.execute('INSERT INTO ' + group_name + ' (Id) VALUES (?)', (member_id,))

    db.commit()


def get_groups():
    db = get_db()
    cursor = db.execute('SELECT Name, Priority FROM groups ORDER BY Id DESC')
    groups = list()
    for row in cursor.fetchall():
        groups.append(dict(name=row[0], priority=row[1]))
    return groups


def get_group_members(group_name):
    db = get_db()
    cursor = db.execute('SELECT Id, Answered FROM ' + group_name + ' ORDER BY Id DESC')
    groups = list()
    for member in cursor.fetchall():
        member_info = db.execute('SELECT FirstName, LastName, Email FROM signups '
                                 'WHERE ID = ' + str(member[0])).fetchone()

        if not member_info: break
        groups.append(dict(name=member_info[0] + " " + member_info[1],
                           email=member_info[2],
                           answered=member[1]))
    return groups