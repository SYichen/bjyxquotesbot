import json
import random
import tweepy
import credentials
import time
import sys
from os import environ

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
	if quote['type'] == "single":
		tweet = """
				{} -{}
				""".format(quote['quote'], quote['who'])
	if quote['type'] == "dialogue" or quote['type'] == "general":
		tweet = """
				{}
				""".format(quote['quote'])
	if len(previouslyPosted) >24:
		previouslyPosted = previouslyPosted[1:]
	previouslyPosted.append(quote['id'])
	return tweet

def tweet_quote():
	interval = 60
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	while True:
		tweet = createTweet()
		api.update_status(tweet)
		time.sleep(interval)

if __name__ == "__main__":
	tweet_quote()