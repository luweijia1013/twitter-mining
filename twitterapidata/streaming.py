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


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    tweets = []
    tweets_num = 0

    def on_data(self, data):
        tweet = json.loads(data, parse_float = decimal.Decimal)
        #print(tweet['text'])
        if tweet['lang']:# == 'en':
            StdOutListener.tweets.append(tweet)
            #StdOutListener.tweets.append(' '.join(tweet['text'].split()))
            # print(' '.join(tweet['text'].split()))
            # with open('data/apple', 'a') as f:
            #     f.write(' '.join(tweet['text'].split())+'\n')

            StdOutListener.tweets_num += 1
            print(StdOutListener.tweets_num)
            STEP = 1
            if len(StdOutListener.tweets) > 0 and len(StdOutListener.tweets) % STEP == 0:
                with open('data/rateairqualityitest','a') as f:
                    for i in range(STEP):
                        json.dump(StdOutListener.tweets.pop(0),f)
                        #f.write(StdOutListener.tweets.pop(0).encode('utf-8'))
                        f.write('\n'.encode('utf-8'))
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
            stream.filter(track=['#rateairqualitytest'])
        except (ProtocolError, AttributeError):
            continue
