import json
import random
import tweepy
#import credentials
import time
import sys
from os import environ

random.seed(8051005)

consumer_key = environ['API_KEY']
consumer_secret_key = environ['API_SECRET_KEY']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

previouslyPosted = []

def getRandomQuote():
	with open('data.json') as f:
		quotes = json.load(f)['bjyxquotes']

	randomQuote = random.choice(quotes)

	while randomQuote['id'] in previouslyPosted:
		randomQuote = random.choice(quotes)

	print(randomQuote)
	return randomQuote

def createTweet():
	global previouslyPosted
	quote = getRandomQuote()
	tweet = """
			{}
			""".format(quote['quote'])
	if len(previouslyPosted) >48:
		previouslyPosted = previouslyPosted[1:]
	print("previouslyPosted:", previouslyPosted)
	print("adding:", quote['id'])
	previouslyPosted.append(quote['id'])
	return tweet

def tweet_quote():
	interval = 60*60
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	while True:
		tweet = createTweet()
		try:
			api.update_status(tweet)
			time.sleep(interval)
		except Exception as e:
			print(e)
			time.sleep(10)

if __name__ == "__main__":
	tweet_quote()