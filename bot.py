import os
import tweepy

consumer_key = os.environ['SINE_CONSUMER_KEY']
consumer_secret = os.environ['SINE_CONSUMER_SECRET']
access_token = os.environ['SINE_ACCESS_KEY']
access_secret = os.environ['SINE_ACCESS_SECRET']

omaega_sine = "@{} お前が死ね"
search = "死ね"

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.me = self.api.me()
    def on_status(self, status):
        if not status.retweeted:
            if search in status.text:
                # print(status)
                print("============================================================")
                print(status.user.name, "@"+status.user.screen_name)
                print("------------------------------------------------------------")
                print(status.text)
                # status._api.update_status(omaega_sine.format(status.user.screen_name), in_reply_to_status_id=status.id)
    def on_event(self, event):
        if event.event == 'follow':
            source_user = event.source
            if self.me.id != source_user["id"]:
                print("============================================================")
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

    u_stream = tweepy.Stream(auth=api.auth, listener=StreamListener(api))
    f_stream = tweepy.Stream(auth=api.auth, listener=StreamListener(api))

    u_stream.userstream(track=search)
    # f_stream.filter(track=search, async=True)
    print("yeah")
