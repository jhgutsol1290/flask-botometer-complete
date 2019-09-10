import tweepy
from twitter_client import TwitterAuthenticator

####input your credentials here
consumer_key = 'wtFRuCKCv8uB4zchxPpj0IxF7'
consumer_secret = 'SUPHCNtK7QWe8fKpYwPt11CKQ9vWdGwawrrMaItEFIuuSAe9d1'
access_token = '2205718165-0nE4pGg3XxLVDQztEGdKmmiXfOkFBRPF4D7SDTm'
access_token_secret = 'n9HnBZgoH1gXUWEo8KGYepYkNHi9lyJNe3hnfEvmxxy67'

twitter_authenticator = TwitterAuthenticator(consumer_key, consumer_secret, access_token, access_token_secret)
api = twitter_authenticator.twitterClient()

class Twitter_Info():
    def get_retweets(self, tweet_id):
        retweets = api.retweets(tweet_id, count=10)
        return retweets
    
    def get_statuses(self, screen_name):
        statuses = tweepy.Cursor(api.user_timeline, screen_name=screen_name, include_rts = True).items(50)
        return statuses
    
    def get_tweets(self, q, quantity):
        query = q
        tweets = tweepy.Cursor(api.search, q=query, lang = 'es', tweet_mode='extended').items(quantity)
        return tweets
