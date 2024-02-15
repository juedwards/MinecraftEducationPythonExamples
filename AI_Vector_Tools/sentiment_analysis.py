import tweepy
from textblob import TextBlob
import csv
import schedule
import time
# Twitter API credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Search query and number of tweets to retrieve
query = 'Minecraft Education'
num_tweets = 100

def sentiment_analysis():
    # Retrieve tweets
    tweets = tweepy.Cursor(api.search, q=query, lang='en').items(num_tweets)

    sentiment_data = []

    # Perform sentiment analysis on each tweet
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        sentiment = analysis.sentiment.polarity

        # Classify sentiment as positive, negative, or neutral
        if sentiment > 0:
            sentiment_label = 'Positive'
        elif sentiment < 0:
            sentiment_label = 'Negative'
        else:
            sentiment_label = 'Neutral'

        # Store tweet and sentiment in a list
        sentiment_data.append([tweet.text, sentiment_label])

    # Write sentiment data to a CSV file
    with open('sentiment.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet', 'Sentiment'])
        writer.writerows(sentiment_data)

    print('Sentiment analysis completed and data stored in sentiment.csv')

# Schedule the sentiment analysis to run every hour
schedule.every().hour.do(sentiment_analysis)

while True:
    schedule.run_pending()
    time.sleep(1)
