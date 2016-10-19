import os, time, datetime, threading
import tweepy

from logging import getLogger,StreamHandler,DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

consumer_key = os.environ['SINE_CONSUMER_KEY']
consumer_secret = os.environ['SINE_CONSUMER_SECRET']
access_token = os.environ['SINE_ACCESS_KEY']
access_secret = os.environ['SINE_ACCESS_SECRET']

omaega_sine = "@{} お前が死ね"
query = "死ね"
ng_words = ["RT", "死ねない"]
ng_names = ["bot", "BOT", "Bot"]

class FollowStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__(api)
        self.me = self.api.me()
    def on_event(self, event):
        if event.event == 'follow':
            source_user = event.source
            print("aa")
            if self.me.id != source_user["id"]:
                print("============================================================")
                print("followed by {} {}".format(source_user["name"], source_user["id"]))
                event._api.create_friendship(source_user["id"])
                print("followed {} {}".format(source_user["name"], source_user["id"]))
    def on_error(self, status_code):
        if status_code == 420:
            print(str(status_code))
            return False

class TweetCrawler(threading.Thread):
    def __init__(self, api, ng_names, ng_words, latest_tweet_id=None, cooltime=10):
        super().__init__(daemon=True)
        self.api = api
        self.ng_names = ng_names
        self.ng_words = ng_words
        self.latest_tweet_id = latest_tweet_id
    def tweet_filter(self, tweet):
        if tweet.retweeted:
            return False
        for ngn, ngw in zip(self.ng_names, self.ng_words):
            if ngn in tweet.user.name or ngw in tweet.text:
                return False
        else:
            return True
    def tweet_crawl(self):
        logger.info("crawling")
        for i, tweet in enumerate(self.api.search(q=query, count=100)):
            if self.latest_tweet_id == None:
                self.latest_tweet_id = tweet.id
            if i == 0:
                new_latest_tweet_id = tweet.id
            if tweet.id > self.latest_tweet_id:
                if self.tweet_filter(tweet):
                    logger.info("{} {} {} {}\n{}\n".format(tweet.created_at, tweet.id, tweet.user.name, tweet.user.screen_name, tweet.text))
            else:
                break
        self.latest_tweet_id = new_latest_tweet_id
    def run(self):
        while True:
            self.tweet_crawl()
            time.sleep(10)

class TweetUpdater(threading.Thread):
    def run(self):
        while True:
            pass

if __name__ == "__main__":
    logger.info("hello")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    u_stream = tweepy.Stream(auth=api.auth, listener=FollowStreamListener(api))

    crawler = TweetCrawler(api, ng_names, ng_words)
    crawler.start()

    while True:
        try:
            u_stream.userstream(track=query)
        except:
            u_stream = tweepy.Stream(auth=api.auth, listener=FollowStreamListener(api))

    logger.info("yeah")
