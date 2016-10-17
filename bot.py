import os

import requests
from requests_oauthlib import OAuth1

import tweepy

import json

consumer_key = os.environ['SINE_CONSUMER_KEY']
consumer_secret = os.environ['SINE_CONSUMER_SECRET']
access_token = os.environ['SINE_ACCESS_KEY']
access_secret = os.environ['SINE_ACCESS_SECRET']

class DotAccessible(object): # http://d.hatena.ne.jp/karasuyamatengu/20120408/1333862237
    """オブジェクトグラフ内の辞書要素をプロパティ風にアクセスすることを可能にするラッパー。
        DotAccessible( { 'foo' : 42 } ).foo==42

    メンバーを帰納的にワップすることによりこの挙動を下層オブジェクトにも与える。
        DotAccessible( { 'lst' : [ { 'foo' : 42 } ] } ).lst[0].foo==42
    """

    def __init__(self, obj):
        self.obj=obj

    def __repr__(self):
        return "DotAccessible(%s)" % repr(self.obj)

    def __getitem__(self, i):
        """リストメンバーをラップ"""
        return self.wrap(self.obj[i])

    def __getslice__(self, i, j):
        """リストメンバーをラップ"""

        return map(self.wrap, self.obj.__getslice__(i,j))

    def __getattr__(self, key):
        """辞書メンバーをプロパティとしてアクセス可能にする。
        辞書キーと同じ名のプロパティはアクセス不可になる。
        """

        if isinstance(self.obj, dict):
            try:
                v=self.obj[key]
            except KeyError:
                v=self.obj.__getattribute__(key)
        else:
            v=self.obj.__getattribute__(key)

        return self.wrap(v)

    def wrap(self, v):
        """要素をラップするためのヘルパー"""

        if isinstance(v, (dict,list,tuple)): # xx add set
            return self.__class__(v)
        return v

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.me = self.api.me()
    def on_status(self, status):
        if "死ね" in status.text:
            print("==============")
            print(status.user.name)
            print("--------------")
            print(status.text)

    def on_event(self, event):
        if event.event == 'follow':
            source_user = event.source
            if self.me.id != source_user["id"]:
                print("followed by {} {}".format(source_user["name"], source_user["id"]))
                event._api.create_friendship(source_user["id"])
                print("followed {} {}".format(source_user["name"], source_user["id"]))
        # if event.event == 'unfollow':
        #     target_user = event.target
        #     print("unfollowed by {} {}".format(target_user["name"], target_user["id"]))
        #     event._api.destroy_friendship(target_user["id"])
        #     print("unfollowed {} {}".format(target_user["name"], target_user["id"]))

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
