"""
REQUIREMENTS: Twython
"""
from twython import Twython
from twython import TwythonError
from twython import TwythonRateLimitError
import time
import os
import json
import datetime
import re


class TwitterAPI():

    def __init__(self):
        """Initialise instance of Twitter Scraper

        :param consumer_key: Used to authorize requests to the Twitter API
        :param consumer_secret: Used to authorize requests to the Twitter API
        :param access_token_key: Used to authorize requests to the Twitter API
        :param access_token_secret: Used to authorize requests to the Twitter API
        """

        # self.consumer_key = 'ZqNtCbyxoWMAkqvEUVeuVbJzM'
        # self.consumer_secret = '25NKzjVS9AT5KKqMBG8XZqiBYbUvb5aVOkuTihFJphwpscDdGZ'
        # self.access_token_key = '1091008892866318337-RvNvRsrMR4sADqM3b2Rbe4Z63Q8ruh'
        # self.access_token_secret = 'ZndXLIfY1t4Jq7HH9fTVWIqZCmjl0dazykRuEtQhh7JCI'
        self.consumer_key = '0PmaM0QgDLKCUnzQxFlBPD5Mx'
        self.consumer_secret = 'NFtjDYpYJgnmUQverFcQJMFt6x9fduJPG9MkjybfAsteaKq1ng'
        self.access_token_key = '449060412-KGZ1sg1cqPCsyWrEZPYkiLkgX19uF4R3ruvzXdnD'
        self.access_token_secret = 'KuiSKD82mpyPWCYZk3kUEv2eIcUOqwC7xujdvXRvaILLC'
        self.dir_path = os.path.realpath(os.path.dirname(__file__))
        try:
            print('Starting Twitter scraper')
            self.twitter = Twython(oauth_token=self.access_token_key, oauth_token_secret=self.access_token_secret, app_key=self.consumer_key,
                                   app_secret=self.consumer_secret)
            print('Successfully started twitter scraper.')
        except Exception as e:
            print('Failed to start twitter scraper. Exception: ' + str(e))
            quit(-1)

    def search_tweets(self, text, total):
        """
        Searching for tweets matching text.
        :param text: The text used to search for tweeys
        :param total: Limits the amount of tweets searched for (i.e. if you put total = 1000, it will only return the first 1000 tweets)
        :return list of tweet dictionaries: full tweet info from twitter api ( read documentation )
        """
        print('Searching for tweets with ' + text)
        if total == None:
            total = 10000
        max_id=-1
        total_tweets = []
        since_id = None
        while len(total_tweets) < total:
            for i in range(0, 2):
                try:
                    new_tweets = []
                    if max_id <= 0:
                        if not since_id:
                            new_tweets = self.twitter.search(q=text, geocode="51.5,-0.127474,10mi", lang="en", count=100, tweet_mode='extended')
                        else:
                            new_tweets = self.twitter.search(q=text, geocode="51.5,-0.127474,10mi", lang="en", count=100, max_id=str(max_id-1), tweet_mode='extended')
                    else:
                        if not since_id:
                            new_tweets = self.twitter.search(q=text, geocode="51.5,-0.127474,10mi", lang="en", count=100, max_id=str(max_id-1), tweet_mode='extended')
                        else:
                            new_tweets = self.twitter.search(q=text, geocode="51.5,-0.127474,10mi", lang="en", count=100, max_id=str(max_id-1), since_id=since_id,tweet_mode='extended')
                    if len(new_tweets['statuses']) == 0:
                        print('No new tweets. Collected ' + str(len(total_tweets)) + ' tweets.')
                        return total_tweets
                    total_tweets.extend(new_tweets['statuses'])
                    max_id = total_tweets[-1]['id']
                    since_id = new_tweets['search_metadata']['since_id']
                    break
                except TwythonRateLimitError as e:
                    remainder = float(self.twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                    print('Hit rate limiter. Sleeping for ' + str(remainder/60) + ' minutes')
                    print(str(len(total_tweets)) + ' tweets are now collected')
                    if remainder > 0:
                        time.sleep(int(remainder) + 5)
                        continue
                    continue
            if len(total_tweets) % 100 == 0:
                print('Collected ' + str(len(total_tweets)) + ' tweets so far...')
        print('Collected maximum amount of tweets. ' + str(len(total_tweets)) + ' collected.')
        return total_tweets

    def get_user_tweets(self, user_id):
        """
        Searching for tweets by a user matching user_id
        :param user_id: Used to search for tweets by same user
        :return tweet dictionary: dictionary containing tweet_id, tweet, retweet_count,likes,date,user_dict
        and a list of retweet users
        """
        print('Collecting user tweets.')
        user_timeline = self.twitter.get_user_timeline(user_id=user_id, tweet_mode='extended')
        user_tweets = []
        if user_timeline != None:
            for tweet in user_timeline:
                try:
                    user = dict(user_id=tweet['user']['id'], name=tweet['user']['name'],
                        screen_name=tweet['user']['screen_name'], follower_count=tweet['user']['followers_count'],
                        total_tweets=tweet['user']['statuses_count'],following=tweet['user']['friends_count'])
                    if 'full_text' in tweet.keys():
                        tw_dict = dict(tweet_id=tweet['id'], tweet=tweet['full_text'],
                                       retweet_count=tweet['retweet_count'],
                                       likes=tweet['favorite_count'], date=tweet['created_at'], user=user)
                    else:
                        tw_dict = dict(tweet_id=tweet['id'], tweet=tweet['text'], retweet_count=tweet['retweet_count'],
                                       likes=tweet['favorite_count'], date=tweet['created_at'], user=user)
                    retweet_ids = []
                    retweet_users = []
                    retweets = self.twitter.get_retweeters_ids(id=tweet['id'])
                    retweet_ids.extend(retweets['ids'])
                    print('Collecting retweet users for tweet.')
                    for retweet_user_id in retweet_ids:
                        users = self.twitter.lookup_user(user_id=retweet_user_id)
                        for user in users:
                            retweet_users.append(dict(user_id=user['id'], name=user['name'], screen_name=user['screen_name'],
                                     follower_count=user['followers_count'], total_tweets=user['statuses_count'],
                                     following=user['friends_count'], retweet_original_id=tweet['id']))
                    tw_dict['retweet_users'] = retweet_users
                    user_tweets.append(tw_dict)
                except TwythonRateLimitError as e:
                    remainder = float(self.twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                    print('Hit rate limiter. Sleeping for ' + str(remainder/60) + ' minutes')
                    if remainder > 0:
                        time.sleep(int(remainder) + 5)
                        continue
                    continue
                except TwythonError as e:
                    print(str(e))
        print('Finished collecting user tweets.')
        return user_tweets

    def search_for_user(self, screen_name):
        """
        Searching for user by screen name.
        :param screen_name: screen name of a twitter user.
        :return user_dict: dictionary containing user_id, name,screen_name, follower_count, total_tweets, following
        """
        for i in range(0,2):
            try:
                users = self.twitter.lookup_user(screen_name=screen_name)
                for user in users:
                    return dict(user_id=user['id'], name=user['name'], screen_name=user['screen_name'],
                                follower_count=user['followers_count'], total_tweets=user['statuses_count'],
                                following=user['friends_count'])
            except TwythonRateLimitError as error:
                remainder = float(self.twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                print('Hit rate limiter. Sleeping for ' + str(remainder/60) + ' minutes ')
                if remainder > 0:
                    time.sleep(int(remainder) + 5)
                    continue
                continue
            except TwythonError as e:
                print('Failed obtaining user information for ' + screen_name)
                print(str(e))

    def get_retweet_users(self, tweet_dict):
        """
        Get the retweet users for any tweet that has been retweeted
        :param tweet_dict:
        :return retweet_users:
        """
        print('Collecting retweet users')
        retweet_users = []
        retweet_ids = None
        for i in range(0,3):
            try:
                retweet_ids = self.twitter.get_retweeters_ids(id=tweet_dict['tweet_id'])
                break
            except Exception as e:
                remainder = float(self.twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                print('Hit rate limiter. Sleeping for ' + str(remainder/10) + ' minutes ')
                if remainder > 0:
                    time.sleep(int(remainder) + 5)
                else:
                    time.sleep(5)

        if retweet_ids != None:
            for retweet_id in retweet_ids['ids']:
                for i in range(0,2):
                    try:
                        users = self.twitter.lookup_user(user_id=retweet_id)
                        if users != None:
                            for user in users:
                                user = dict(user_id=user['id'], name=user['name'],
                                            screen_name=user['screen_name'], followers_count=user['followers_count'],
                                            total_tweets=user['statuses_count'], following=user['friends_count'])
                                retweet_users.append(user)
                        break
                    except Exception as e:
                        remainder = float(self.twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                        print('Hit rate limiter. Sleeping for ' + str(remainder/60) + ' minutes ')
                        if remainder > 0:
                            time.sleep(int(remainder) + 5)
                        else:
                            time.sleep(5)
            print('Collected ' + str(len(retweet_users)) + ' users.')
        return retweet_users

    def get_original_tweet(self, retweet):
        """
        Takes the retweet and finds the original tweet
        :param retweet:
        :return original tweet:
        """
        print('Obtaining original tweet.')
        tweet = None
        for i in range(0, 2):
            try:
                original_tweet = self.twitter.show_status(id=retweet['retweeted_status']['id'])
                if original_tweet != None:
                    tweet = original_tweet
                    print('Found original tweet!')
                break
            except Exception as e:
                remainder = float(self.twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                print('Hit rate limiter. Sleeping for ' + str(remainder/60) + ' minutes ')
                if remainder > 0:
                    time.sleep(int(remainder) + 5)
                else:
                    time.sleep(5)
        return tweet

    def collector(self, text, total):
        """
        Collects tweets based on text, finds original tweet if it's a retweet
        and then collects retweet users if it's a retweet.
        Filters the fields for both tweet and user.
        :param text: Used to search for tweets
        :param total: Limits the amount of tweets searched for
        :return filtered_tweets:  list of dictionaries of tweet info with user and retweet user info
        """
        filtered_tweets = []
        tweets = self.search_tweets(text, total)
        seen_tweets = []
        for tweet in tweets:
            # if 'retweeted_status' in tweet.keys():
            #     tweet = self.get_original_tweet(tweet)

            if tweet['id'] not in seen_tweets:
                seen_tweets.append(tweet['id'])
                user = tweet['user']
                place = tweet['place']
                user = dict(user_id=user['id'], name=user['name'])
                            # screen_name=user['screen_name'], 
                            #followers_count=user['followers_count'],
                            #total_tweets=user['statuses_count'],
                            #following=user['friends_count'])
                if 'full_text' in tweet.keys():
                    tweet_dict = dict(tweet_id=tweet['id'], tweet=tweet['full_text'],
                                      date=tweet['created_at'], user=user, place = place)#, retweet_count=tweet['retweet_count'])
                else:
                    tweet_dict = dict(tweet_id=tweet['id'], tweet=tweet['text'],
                                      date=tweet['created_at'], user=user)#, retweet_count=tweet['retweet_count'])

                # if tweet_dict['retweet_count'] > 0:
                #     retweet_users = self.get_retweet_users(tweet_dict)
                #     tweet_dict['retweet_users'] = retweet_users
                if len(tweet_dict['tweet']) > 10: #and tweet_dict['place']:# and tweet_dict['place']['country_code']=='GB':
                    filtered_tweets.append(tweet_dict['date'] + ' ***** ' + tweet_dict['tweet']) #tweet_dict['place']['name'] + '  ****** ' +
        return filtered_tweets

def parseTweet(line):
    line = ' '.join(re.sub("(@[_A-Za-z0-9]+)|(#[_A-Za-z0-9]+)", " ", line).split())
    line = ' '.join(re.sub("(\w+:\/\/\S+)", " ", line).split())
    line = line.replace('RT :','').replace('RT ','')
    return line


if __name__ == '__main__':
    api = TwitterAPI()
    searchText = 'air quality'
    tweets = api.collector(searchText, 10000)
    TIMEFORMAT = '%Y%m%d_%H%M'
    theTime = datetime.datetime.now().strftime(TIMEFORMAT)
    tweets_set = set()
    for tweet in tweets:
        tweet = ' '.join(tweet.split())
        tweets_set.add(tweet)
    if(len(tweets)>0):
        with open('data/THESIS_' + searchText + '_' + theTime , 'w') as f:
            # json.dump(tweets, f)
            for tweet in tweets_set:
                # tweet = tweet.encode("UTF-8")
                # tweet = parseTweet(tweet)
                # print(tweet)
                f.write(tweet)
                f.write('\n')
