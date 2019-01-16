from watson_developer_cloud import ToneAnalyzerV3
from collections import Counter
from dateutil import parser

import json
import datetime
import requests
import twitter

# used python-twitter api to get tweets
# used IBM Watson api to do sentiment analysis
# used AlphaVantage api to get stock prices

# Twitter access tokens
ACCESS_TOKEN_KEY = '334444072-Xj2lrc5Xh51bRi4xvadXwhdyzI7mAhCLyWJEzzYr'
ACCESS_TOKEN_SECRET = 'wwSKRsN47dWjfFcQbkPTGp2lnljbNIhmMPaOEeWlf3ssp'
CONSUMER_KEY = 'i4ZrOiOLqZ2gKwu0r76FvhB7z'
CONSUMER_SECRET = '70ssfAJraZ1s8qx0nkGxLohXWQkGvZD00n5w0sL71w1m8HSLxs'

# helper function to get all tweets up to max allowed 3,200
# currently returning 200 most recent tweets
def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    # print("getting tweets before:", earliest_tweet)
    print('Getting 200 most recent tweets \n')

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        # else:
        #     earliest_tweet = new_earliest
        #     print("getting tweets before:", earliest_tweet)
        #     timeline += tweets
        break
    return timeline


# dictionary of tweets indexed on date
# will contain following structure:
# [[list of sentiment for days tweets], stock_market_close - stock_market_open]
trump_tweets = {}

# pull all tweets
api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
screen_name = 'realDonaldTrump'
timeline = get_tweets(api=api, screen_name=screen_name)

# create ToneAnalyzer IBM Watson object
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='n54NtzfmzFug46PryonqHU9sGWWaGKcT_vQ_zQhOvdrR',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)
first_tweet = 0
earliest_date = ''
recent_date = ''

# add tweets and sentiment to dictionary
for tweet in timeline:

    dt = parser.parse(tweet._json['created_at'])
    date = datetime.datetime.strptime(str(dt.day) + str(dt.month) + str(dt.year), '%d%m%Y').date()

    if first_tweet == 0:
        recent_date = date
        first_tweet = 1

    earliest_date = date

    # IBM Watson tone analysis on each tweet
    tone_analysis = tone_analyzer.tone(
        {'text': tweet._json['full_text']},
        'application/json',
        False
    ).get_result()

    if len(tone_analysis['document_tone']['tones']) == 0:
        continue

    print('Detected sentiment ' + tone_analysis['document_tone']['tones'][0]['tone_name'] + ' in tweet')

    if str(date) not in trump_tweets:
        trump_tweets[str(date)] = [[tone_analysis['document_tone']['tones'][0]['tone_name']]]
        # trump_tweets[str(date)] = [[tweet._json['full_text']]]
    else:
        # trump_tweets[str(date)][0].append(tweet._json['full_text'])
        trump_tweets[str(date)][0].append(tone_analysis['document_tone']['tones'][0]['tone_name'])


# pulling historic S&P 500 data
url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPX&outputsize=full&apikey=1TTCW4N7SLIUCIWS"

print('pulling historic stock prices')

stockResponse = requests.get(url)
jData = json.loads(stockResponse.content)

for date in jData['Time Series (Daily)']:
    if date in trump_tweets:
        dated_tweets = trump_tweets[date]
        open = jData['Time Series (Daily)'][date]['1. open']
        close = jData['Time Series (Daily)'][date]['4. close']
        dated_tweets.append(float(open)-float(close))

print('\n')
print(trump_tweets.keys())
print('\n')

# user input - enter date from the printed list to find most common sentiment for the day and S&P 500 close
while True:
    date = input("Please enter a date from the above printed list to find most common "
                 "Trump tweet sentiment or leave a blank line to quit: ")
    if not date: break

    if date not in trump_tweets:
        print('No tweets from trump on ' + str(date) + ' :/')

    elif len(trump_tweets[date]) == 1:

        data = Counter(trump_tweets[date][0])
        print('Trump sentiment for the day was ' + data.most_common(1)[0][0] + ' but markets were closed')

    else:

        data = Counter(trump_tweets[date][0])
        if trump_tweets[date][1] >= 0:
            print('Trump sentiment for the day was ' + data.most_common(1)[0][0] + ' and S&P 500 closed up $' + str("%.2f" % trump_tweets[date][1]))
        else:
            print('Trump sentiment for the day was ' + data.most_common(1)[0][0] + ' and S&P 500 closed down $' + str("%.2f" % trump_tweets[date][1]))
