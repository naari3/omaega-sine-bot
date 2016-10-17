import os

import requests
from requests_oauthlib import OAuth1

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

filter_url = "https://stream.twitter.com/1.1/statuses/filter.json"
user_url = "https://userstream.twitter.com/1.1/user.json"

auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)

f_r = requests.post(filter_url, auth=auth, stream=True, data={"track":"死ね"})
u_r = requests.post(user_url, auth=auth, stream=True, data={"track":"死ね"})

# for line in f_r.iter_lines():
#     if line == b'':
#         continue
#     tw = json.loads(line.decode('utf-8'))
#     # print(tw)
#     tweet = DotAccessible(tw)
#     if not tweet.retweeted:
#         print("==============================")
#         print(tweet.user.name)
#         print("------------------------------")
#         print(tweet.text)

for line in u_r.iter_lines():
    if line == b'':
        continue
    tw = json.loads(line.decode('utf-8'))
    if tw.get("friends", None):
        continue
    if tw.get("delete", None):
        continue
    tweet = DotAccessible(tw)

    if tw.get("event", None):
        print("==============================")
        print("¥¥¥¥¥¥¥¥¥¥¥¥")
        print(tweet)
        continue
    if not tweet.retweeted:
        print("==============================")
        print(tweet.user.name)
        print("------------------------------")
        print(tweet.text)
        continue
