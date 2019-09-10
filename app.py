from flask import Flask, render_template, request, redirect, url_for, flash, session
from twitter_client import TwitterAuthenticator
from botometer_class import Bot_Detector
from retweets_class import Retweeters
from tweepy_class import Twitter_Info
from data_class import Data_Accounts

app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def home():   
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        f = request.files['fileupload']
        if not f:
            return render_template('error.html', data={'message': 'No seleccionaste archivo a evaluar'})
        botometer = Bot_Detector()
        array_screen_names = botometer.read_csv_file(f)
        if array_screen_names:
            scores_complete = botometer.get_scores_complete(array_screen_names)
            data = scores_complete
            return render_template('show.html', data=data)
        elif not array_screen_names:
            return render_template('error.html', data={'message': 'Demasiadas cuentas, deben ser máximo 300 por consulta'})
        

@app.route('/retweet')
def home_retweet():   
    return render_template('search-retweet.html')

@app.route('/search-retweet', methods=['POST'])
def search_retweet():
    if request.method == 'POST':
        tweet_id = int(request.form['tweet_id'])
        twitter = Twitter_Info()
        retweets_get = Retweeters()
        botometer = Bot_Detector()
        retweets = twitter.get_retweets(tweet_id)
        array_accounts = retweets_get.get_array_screen_names(retweets)
        scores_complete = botometer.get_scores_complete(array_accounts)
        data = scores_complete
        return render_template('show.html', data=data)


@app.route('/tweet')
def home_tweet():
        return render_template('search-tweet.html')

@app.route('/search-tweet', methods=['POST'])
def search_tweet():
    if request.method == 'POST':
        query_search = ''
        term = request.form['term']
        items = int(request.form['items'])
        retweets = int(request.form['retweets'])
        if retweets == 1:
                query_search = str(term + ' -filter:retweets')
        elif retweets == 2:
                query_search = str(term)
        data_twitter = Data_Accounts()
        data_tweets = data_twitter.get_data_from_tweets(query_search, items)  
        data = data_tweets  
        return render_template('show-tweet.html', data=data)        


if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0', debug=True)