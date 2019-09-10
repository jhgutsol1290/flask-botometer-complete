import botometer
import tweepy
import pandas as pd
import numpy as np
from twitter_client import TwitterAuthenticator
from tweepy_class import Twitter_Info

####input your credentials here
consumer_key = 'wtFRuCKCv8uB4zchxPpj0IxF7'
consumer_secret = 'SUPHCNtK7QWe8fKpYwPt11CKQ9vWdGwawrrMaItEFIuuSAe9d1'
access_token = '2205718165-0nE4pGg3XxLVDQztEGdKmmiXfOkFBRPF4D7SDTm'
access_token_secret = 'n9HnBZgoH1gXUWEo8KGYepYkNHi9lyJNe3hnfEvmxxy67'

twitter_authenticator = TwitterAuthenticator(consumer_key, consumer_secret, access_token, access_token_secret)
api = twitter_authenticator.twitterClient()

rapidapi_key = "c9a184ffb5msh1d1b9dc6c2099f5p18746cjsn05cfff51b87d" # now it's called rapidapi key
twitter_app_auth = {
    'consumer_key': 'wtFRuCKCv8uB4zchxPpj0IxF7',
    'consumer_secret': 'SUPHCNtK7QWe8fKpYwPt11CKQ9vWdGwawrrMaItEFIuuSAe9d1',
    'access_token': '2205718165-0nE4pGg3XxLVDQztEGdKmmiXfOkFBRPF4D7SDTm',
    'access_token_secret': 'n9HnBZgoH1gXUWEo8KGYepYkNHi9lyJNe3hnfEvmxxy67',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

class Bot_Detector():
    def __init__(self, array_scores = [], array_accounts_not_found = [], array_scores_complete = [], acc = [], dfToList = []):
        self.array_scores = []
        self.array_accounts_not_found = []
        self.array_scores_complete = []
        self.acc = []
        self.dfToList = []
    
    def read_csv_file(self, file):
        df = pd.read_csv(file, header=None, names=['screen_names'])
        self.dfToList = df['screen_names'].tolist()
        self.acc = ['@' + element for element in self.dfToList]
        if len(self.acc) > 10:
            return False
        elif len(self.acc) <= 10:
            return self.acc
    
    def get_scores_complete(self, array_screen_names):
        for screen_name, result in bom.check_accounts_in(array_screen_names):
            try:
                data = result['display_scores']
                self.array_scores.append(data['user'])
                twitter = Twitter_Info()
                if data['user'] >= 2.5:
                    twitter_info = api.get_user(result['user']['screen_name'])
                    #statuses = tweepy.Cursor(api.user_timeline, screen_name=result['user']['screen_name'], include_rts = True).items(50)
                    statuses = twitter.get_statuses(result['user']['screen_name'])
                    retweeted = 0
                    min_sec_array = []
                    dates_array = []
                    flag = 0
                    for status in statuses:
                        if 'RT' in status.text:
                            retweeted += 1
                        dates_array.append(status.created_at)
                    for i in range(len(dates_array) - 1):
                        res = dates_array[i] - dates_array[i + 1]
                        min_sec_array.append(res.seconds)
                        flag = min(min_sec_array)
                    percentage_retweets = round((retweeted / twitter_info.statuses_count) * 100, 1)
                    self.array_scores_complete.append({'screen_name': screen_name, 'content': data['content'], 'friend': data['friend'], 'network': data['network'], 'sentiment': data['sentiment'], 'temporal': data['temporal'], 'user': data['user'], 'status': 'Bot', 'followers': twitter_info.followers_count, 'following': twitter_info.friends_count, 'favourites': twitter_info.favourites_count, 'total_tweets': twitter_info.statuses_count, 'retweets': retweeted, 'percentage_retweets': percentage_retweets, 'less_time_bet_tweets': flag})
                elif data['user'] < 2.5:
                    self.array_scores_complete.append({'screen_name': screen_name, 'content': data['content'], 'friend': data['friend'], 'network': data['network'], 'sentiment': data['sentiment'], 'temporal': data['temporal'], 'user': data['user'], 'status': 'Real Account'})
            except KeyError:
                self.array_accounts_not_found.append(screen_name)
        #quantities = self.get_quantity_bots_and_real_accounts()
        return [self.array_scores_complete, self.array_accounts_not_found]
    
    def get_quantity_bots_and_real_accounts(self):
        array_scores_bots = [element for element in self.array_scores if element >= 2.5]
        array_scores_real = [element for element in self.array_scores if element < 2.5]
        count_bots = len(array_scores_bots)
        count_real = len(array_scores_real)
        total = count_bots + count_real
        return [array_scores_bots, count_bots, array_scores_real, count_real, total]




