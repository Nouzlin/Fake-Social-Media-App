__author__ = 'linko538'

import facebook
from TwitterAPI import TwitterAPI

# Keys to send information and retrieve information from twitter
api = TwitterAPI(consumer_key="HQxmGENKZkT1hgQZL7tKA",
                 consumer_secret="CR3zzMoZZIhDfV6x0TLrxiYic2lMM6pmJGzLyc3mc4",
                 access_token_key="394882737-cwGoxnV7zmOijWvmHK53oy8Ny4XimLncymDyyTLq",
                 access_token_secret="7E505TL5yUpfIf9pWnpoyfrQz98jCaSZKz5OKw0mMmZzT")

# Tweets out a notice about who signed up to the web-page...
# (Generally a bad idea if you want to avoid getting banned)
def tweet(info):
    api.request('statuses/update', {'status': '#TDDD80' + ' ' + info[0] + ' ' + info[1] +
                                    ' just signed up!'})

# Retrieves the tweets with the given hashtag
# and puts them in a dictionary for easy accessing.
def get_tweets(hashtag):
    r = api.request('search/tweets', {'q': hashtag})
    tweets = [dict(name=info[u'user'][u'name'], text=info[u'text'], location=info[u'user'][u'location'])
              for info in r.get_iterator()]
    return tweets

# Code for sharing a custom made user story onto FB.
# :earn is the Action
# awesomeness is the Object
# (which has some properties you can customize on the FB page)
#TODO: Handle AssertionError "No valid oauth token"
def share_story(oath_token):
    graph = facebook.GraphAPI(oath_token)
    return graph.put_object("me", "linko_lab_three:earn", awesomeness={
        "og:title": "Sample Awesomeness",
        "og:image": "http://larrysnow.me/wp-content/uploads/2013/07/i-want-to-be-number-one-on-google.png",
        "og:description": "Wow much sad",
        "og:type": "linko_lab_three:awesomeness"
        })




