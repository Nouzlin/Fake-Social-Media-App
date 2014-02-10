__author__ = 'linko538'

import facebook
from TwitterAPI import TwitterAPI

api = TwitterAPI(consumer_key="HQxmGENKZkT1hgQZL7tKA",
                    consumer_secret="CR3zzMoZZIhDfV6x0TLrxiYic2lMM6pmJGzLyc3mc4",
                    access_token_key="394882737-cwGoxnV7zmOijWvmHK53oy8Ny4XimLncymDyyTLq",
                    access_token_secret="7E505TL5yUpfIf9pWnpoyfrQz98jCaSZKz5OKw0mMmZzT")

def tweet(info):
    api.request('statuses/update', {'status': '#TDDD80' + ' ' + info[0] + ' ' + info[1] +
                                                  ' just signed up!'})

def get_tweets():
    r = api.request('search/tweets', {'q': '#TDDD80'})
    tweets = [dict(name=info[u'user'][u'name'], text=info[u'text'], location=info[u'user'][u'location'])
              for info in r.get_iterator()]
    return tweets

def share_story(oath_token):
    graph = facebook.GraphAPI(oath_token)
    return graph.put_object("me", "linko_lab_three:earn", awesomeness={
        "og:title": "Sample Awesomeness",
        "og:image": "http://larrysnow.me/wp-content/uploads/2013/07/i-want-to-be-number-one-on-google.png",
        "og:description": "Wow much sad",
        "og:type": "linko_lab_three:awesomeness"
        })




