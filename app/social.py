__author__ = 'linko538'

import facebook
from flask import request

def upload_wall(oath_token):
    graph = facebook.GraphAPI(oath_token)
    profile = graph.get_object("me")
    friends = graph.get_connections("me", "friends")
    return graph.put_object("me", "feed", message="Let the bodies hit the floor!")
