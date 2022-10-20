import html
import os
import time
import tweepy as tp
from telegram import Bot
from telegram import ParseMode
import json
from userslist import *
from dotenv import load_dotenv

load_dotenv("keys.env")
token = str(os.getenv("TELEGRAM_BOT"))
chatid = int(os.getenv("CHAT_ID"))
bearer = str(os.getenv("BEARER_TOKEN"))

class TwitterStream(tp.StreamingClient):

    def on_data(self,data):
        try:
            tb = TweetBot()
            bot = Bot(token=token)
            d = json.loads(data)
            tweet_url = tb.get_tweet_url(json_data=d)
            tg_text = d['data']['text']
            tusername = d['includes']['users'][0]['username']
            tname = d['includes']['users'][0]['name']
            text = "{0}\n\n-- <a href='{1}'>{2}</a>".format(tg_text, tweet_url, tusername)
            print("TwitterStream -- sending: {0}".format(text))
            bot.sendMessage(chat_id=chatid,
                            text=text,
                            timeout=200,
                            disable_web_page_preview=False,
                            parse_mode=ParseMode.HTML
            )
        except Exception as e:
            print(e)

        return True

    def on_error(self,status):
        print(status.text)
        
    def on_error(self,status_code):
        if status_code == 420:
            return False



class TweetBot():

    def __init__(self):
        pass

    def authorize(self):
        consumer_key = str(os.getenv("CONSUMER_KEY"))
        consumer_secret = str(os.getenv("CONSUMER_SECRET"))
        access_token = str(os.getenv("ACCESS_TOKEN"))
        access_token_secret = str(os.getenv("ACCESS_TOKEN_SECRET"))
        bearer_token = str(os.getenv("BEARER_TOKEN"))

        client = tp.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )
        return client


    def fetch_tweets(self):
        api = self.authorize()
        listener = TwitterStream(bearer_token=api.bearer_token)
        print("TweetBot - stream created")
        users_search_string = " OR ".join("from:" + x for x in userslist)
        rule = tp.StreamRule(value=users_search_string)
        listener.add_rules(rule)
        print("TweetBot - rule created")
        listener.filter(expansions="author_id")
        print("TweetBot - filtered")

    def get_tweet_acid(self,user_list):
        api = self.authorize()
        list_id = []
        for i in user_list:
            user = tp.User(api.get_user(username=str(i)).data)
            id = user.id
            list_id.append(str(id))
        return list_id    
    
    def get_tweet_url(self,json_data):
        try:
            return "https://twitter.com/{uname}/status/{tid}".format(uname=json_data['includes']['users'][0]['username'], tid=json_data['data']['id'])
        except:
            return ""  
    
