import os
import tweepy

consumer_key = os.environ['SINE_CONSUMER_KEY']
consumer_secret = os.environ['SINE_CONSUMER_SECRET']
access_token = os.environ['SINE_ACCESS_KEY']
access_secret = os.environ['SINE_ACCESS_SECRET']

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__()
        print(dir(self))
        self.api = api
        self.me = self.api.me()
    def on_status(self, status):
        if "死ね" in status.text:
            print("====================")
            print(status.user.name)
            print("--------------------")
            print(status.text)
    def on_event(self, event):
        if event.event == 'follow':
            source_user = event.source
            if self.me.id != source_user["id"]:
                print("followed by {} {}".format(source_user["name"], source_user["id"]))
                event._api.create_friendship(source_user["id"])
                print("followed {} {}".format(source_user["name"], source_user["id"]))
    def on_error(self, status_code):
        if status_code == 420:
            print(str(status_code))
            return False

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    stream = tweepy.Stream(auth=api.auth, listener=StreamListener(api))

    stream.userstream(track=[u'死ね'])
    print("yeah")
