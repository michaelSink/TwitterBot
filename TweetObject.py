"""
Record class for the purpose of storing contents of tweets.
"""
class TweetObject:
    def __init__(self, tweetID, username, time, message):
        self._obj = {"id" : tweetID, "username" : username,"deadline" : time, "message" : message}

    def get_dict(self):
        return self._obj