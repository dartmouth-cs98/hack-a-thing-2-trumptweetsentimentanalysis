import json
from watson_developer_cloud import ToneAnalyzerV3

import json
import sys

import twitter

ACCESS_TOKEN_KEY = '334444072-Xj2lrc5Xh51bRi4xvadXwhdyzI7mAhCLyWJEzzYr'
ACCESS_TOKEN_SECRET = 'wwSKRsN47dWjfFcQbkPTGp2lnljbNIhmMPaOEeWlf3ssp'
CONSUMER_KEY = 'i4ZrOiOLqZ2gKwu0r76FvhB7z'
CONSUMER_SECRET = '70ssfAJraZ1s8qx0nkGxLohXWQkGvZD00n5w0sL71w1m8HSLxs'

def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


if __name__ == "__main__":
    api = twitter.Api(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
    )
    screen_name = 'realDonaldTrump'
    print(screen_name)
    timeline = get_tweets(api=api, screen_name=screen_name)

    # with open('examples/timeline.json', 'w+') as f:
    for tweet in timeline:
            print(tweet)
            print('\n')