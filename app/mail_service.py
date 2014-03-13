from flask import render_template

__author__ = 'Linus'
from flask.ext.mail import Message
import routes
import cipher

def send_information_email(group_id, members):
    for member in members:
        url = cipher.encrypt_val(group_id, member['id'])
        send_email("Welcome",
                   routes.ADMINS[0],
                   [member['email']],
                   render_template("informative_email.txt",
                                   link=url),
                   render_template("informative_email.html",
                                   link=url))
    return

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    routes.mail.send(msg)