import tweepy
from time import sleep

user_stalk = 'kantudo'

consumer_key = 'Pro9gu4fOV1xMpTE1vqZnuPpP'
consumer_secret = '79vXdPFMnJfhepqiHcBoavW3mH88BH48nsLSQELoYOjFQlFYEc'
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

twits = api.user_timeline(screen_name = user_stalk, count = 2, include_rts = False)
prev_twit = twits[0].id
new_twit = prev_twit

while True:
    twits = api.user_timeline(screen_name = user_stalk, count = 2, include_rts = False)
    new_twit = twits[0].id
    if new_twit != prev_twit:
        prev_twit = new_twit
        print('que pasa jesus')
    sleep(1)
