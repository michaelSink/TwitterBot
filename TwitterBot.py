import datetime
import requests
import re
from dateutil import parser
import TweetObject as twObj

class TwitterBot:
    """
    Input:
        token - Beaer token used for authentication
        userID - user_id of the bot in question
    Output:
        Instance of TwitterBot
    Other:
        since - Used for storing most recently polled tweet ID
    """
    def __init__(self, token, userID, since=""):
        self.userID = userID;
        self._token = token;
        self._since = since;

    """
    Purpose: Find the most recent tweets since self._since and add them to a list
    Input:
        None
    Output:
        tweets - List of TweetObject's to be added to database
    """
    def listen(self):
        try:
            print("Listening for new tweets")

            tweets = []

            headers = {"Authorization": "Bearer " + self._token}
            params = {"since_id" : self._since} if self._since != "" else {}
            params.update({"tweet.fields":"created_at", "user.fields":"username","expansions":"author_id"})

            url = "https://api.twitter.com/2/users/{}/mentions".format(self.userID)

            req = requests.get(url, headers=headers, params=params)
            jsonResp = req.json();

            if 'newest_id' in jsonResp['meta']:
                self._since = jsonResp['meta']['newest_id']

            while req.ok == True and len(jsonResp.keys()) > 1:

                for tweet in jsonResp['data']:
                    time_parse = re.search("(?<![a-zA-Z0-9])([0-9]+[h,m])(?!. | ['\s'])", tweet['text'])

                    if time_parse:

                        time = time_parse.group()
                        tweet_text = tweet['text'][time_parse.end():].lstrip()

                        if(time[-1:] == "m"):
                            delta = datetime.timedelta(minutes=int(time[:-1]))
                        else:
                            delta = datetime.timedelta(hours=int(time[:-1]))

                        dateMade = parser.parse(tweet['created_at'])
                        #print("Created at {}, and has a deadline of {}".format(dateMade, dateMade + delta))
                        tweets.append(twObj.TweetObject(tweet['id'], jsonResp['includes']['users'][0]['username'], dateMade + delta, tweet_text))

                if 'next_token' not in jsonResp['meta']:
                    break;
                else:
                    params['pagination_token'] = jsonResp['meta']['next_token']

                req = requests.get(url, headers=headers, params=params)

                jsonResp = req.json();

        except Exception as e:
            print("Error: {}".format(e));

        return tweets