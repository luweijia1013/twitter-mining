from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from urllib3.exceptions import ProtocolError

# import boto3
import json
import decimal

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = 'ZqNtCbyxoWMAkqvEUVeuVbJzM'
consumer_secret = '25NKzjVS9AT5KKqMBG8XZqiBYbUvb5aVOkuTihFJphwpscDdGZ'
# consumer_key="tTycUYRidT6tx0LqRg7KkvVf3"
# consumer_secret="dA7mlmK8pC3Rjys3angNL71zRpQLmfTb6pxqmCybuhoO5ZLdJK"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = '1091008892866318337-RvNvRsrMR4sADqM3b2Rbe4Z63Q8ruh'
access_token_secret = 'ZndXLIfY1t4Jq7HH9fTVWIqZCmjl0dazykRuEtQhh7JCI'
# access_token="982767300-LraJlggxgvA60h2uVY8TP2vekc3Geu4Ck1NJLNJ6"
# access_token_secret="4Xbkp8pwuDQ9LArejXfdRnsA70lB9CDOg0MF1It54FNGa"
result = []

tweets = []

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        tweet = json.loads(data, parse_float = decimal.Decimal)
        if tweet['lang'] == 'en':
            tweets.append(' '.join(tweet['text'].split()))
        print(len(tweets))
        STEP = 3
        if len(tweets) > 0 and len(tweets) % STEP == 0:
            with open('data/apple','w') as f:
                for i in range(STEP):
                    f.write(tweets.pop(0))
            return True

        # tweet变量就是获取到的数据

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    while True:
        try:
            stream.filter(track=['@apple'])
        except (ProtocolError, AttributeError):
            continue
