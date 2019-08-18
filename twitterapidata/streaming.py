from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from urllib3.exceptions import ProtocolError

# import boto3
import json
import decimal

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
# consumer_key = 'ZqNtCbyxoWMAkqvEUVeuVbJzM'
# consumer_secret = '25NKzjVS9AT5KKqMBG8XZqiBYbUvb5aVOkuTihFJphwpscDdGZ'
consumer_key="tTycUYRidT6tx0LqRg7KkvVf3"
consumer_secret="dA7mlmK8pC3Rjys3angNL71zRpQLmfTb6pxqmCybuhoO5ZLdJK"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
# access_token = '1091008892866318337-RvNvRsrMR4sADqM3b2Rbe4Z63Q8ruh'
# access_token_secret = 'ZndXLIfY1t4Jq7HH9fTVWIqZCmjl0dazykRuEtQhh7JCI'
access_token="982767300-LraJlggxgvA60h2uVY8TP2vekc3Geu4Ck1NJLNJ6"
access_token_secret="4Xbkp8pwuDQ9LArejXfdRnsA70lB9CDOg0MF1It54FNGa"
result = []


class TweetKeyInfo():

    tweet_counts = 0

    def __init__(self, tweetid, createat, text, userid, userhandle, place=None):
        self.id = tweetid
        self.created_at = createat
        self.text = text
        self.user = {'id':userid, 'screen_name':userhandle}
        self.place = place
        TweetKeyInfo.tweet_counts += 1
    #
    # def __init__(self,d):
    #     self.__dict__ = d

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    tweets_keyinfo = []
    raw_data = []
    tweets_num = 0

    def on_data(self, data):
        #data - JsonStr, tweet - python object(dict)
        StdOutListener.raw_data.append(data)
        tweet_dict = json.loads(data)#, parse_float = decimal.Decimal)
        tweet_key = TweetKeyInfo(tweet_dict['id'], tweet_dict['created_at'], tweet_dict['text'], tweet_dict['user']['id'], tweet_dict['user']['screen_name'], tweet_dict['place'])
        StdOutListener.tweets_keyinfo.append(tweet_key)
        StdOutListener.tweets_num += 1

        # if tweet['lang']:# == 'en':
        print(StdOutListener.tweets_num)
        STEP = 1
        if len(StdOutListener.tweets_keyinfo) > 0 and len(StdOutListener.tweets_keyinfo) % STEP == 0:
            with open('data/active/aqrate','a') as f:
                for i in range(STEP):
                    tweet_key = StdOutListener.tweets_keyinfo.pop(0)
                    if tweet_key.place:
                        print('!!!')
                    f.write(json.dumps(tweet_key.__dict__))
                    f.write('\n')
            with open('data/active/aqrate_raw','a') as f:
                for i in range(STEP):
                    rawdata_jsonstr = StdOutListener.raw_data.pop(0)
                    f.write(rawdata_jsonstr)
        return True



    def on_error(self, status):
        print('error',status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    while True:
        try:
            stream.filter(track=['tesla'])
        except (ProtocolError, AttributeError):
            continue
