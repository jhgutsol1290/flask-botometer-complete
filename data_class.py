from tweepy_class import Twitter_Info

class Data_Accounts():
    def __init__(self, tweets_array = []):
        self.tweets_array = []

    def get_data_from_tweets(self, q, quantity):
        twitter = Twitter_Info()
        tweets = twitter.get_tweets(q, quantity)
        for tweet in tweets:
            text_tweet = tweet.full_text.replace('\n', ' ').replace('\r', '')
            link = 'twitter.com/'+str(tweet.user.screen_name)+'/status/'+str(tweet.id)
            self.tweets_array.append({'screen_name': tweet.user.screen_name, 'full_text': text_tweet, 'created': tweet.created_at.strftime("%d/%m/%Y, %H:%M:%S"), 'link': link})
        return self.tweets_array
