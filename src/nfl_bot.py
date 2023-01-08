import tweepy
import time
import requests
from datetime import datetime, timezone


CONSUMER_KEY = 'xq70VA2O00J1pL2PS55IHfnul'
CONSUMER_SECRET = 'OqWvB2ewsjEFjqNvHyES0m1LGILEdnMCS1iVC9gLXsXQbxKNZh'
BEARER_KEY = 'AAAAAAAAAAAAAAAAAAAAAGdUlAEAAAAAeue%2BdYc8w7s5lsjhy38ewWW5iqI%3DEwJgfWgYbNYP8ix7HiO0WvjanV9N62PEGh7Mbg95I8M2jlNnHB'
ACCESS_KEY = '1591691192189816835-GFyw7bO4iR9GnJuJ3pxIk50oW5iqP9'
ACCESS_SECRET = 'qBaazPh5RNvauXW3mTdhZKk82HZTwOU73vfXtxACsueGo'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth) 
date = str(datetime.now(timezone.utc))
month_year = date[5:7] + '/' + date[8:10]
date = date[0:10] + 'T' + date[11:19]
game_date = ''

tweet = ' '
last_tweet = ' '

def nfl_stats():
    url = 'https://fcast.espncdn.com/FastcastService/pubsub/profiles/12000/topic/event-football-nfl/message/2631873/checkpoint'

    r = requests.get(url)
    data = r.json()
    headers = data["sports"][0]["leagues"][0]["events"]

    for i in headers:
        if ("KC" in i["shortName"]):
            last_play = i["situation"]["lastPlay"]["text"][8:]
            down = i["situation"]["downDistanceText"]
            clock = i["summary"]

            if(i["competitors"][0]["abbreviation"] == "KC"):
                score = i["competitors"][0]["abbreviation"] + ': ' + str(i["competitors"][0]["score"]) + '\n' + i["competitors"][1]["abbreviation"] + ': ' + i["competitors"][1]["score"]
            else:
                score = i["competitors"][1]["abbreviation"] + ': ' + str(i["competitors"][1]["score"]) + '\n' + i["competitors"][0]["abbreviation"] + ': ' + i["competitors"][0]["score"]

            this_tweet = down + '\n' + last_play + '\n' + '\n' + score + '\n' + clock



    return this_tweet

while True:
    tweet = nfl_stats()
    if last_tweet == tweet:
        print(tweet)
        continue
    else:
        #api.update_status(tweet)
        print(tweet)
        last_tweet = tweet
    time.sleep(5)


