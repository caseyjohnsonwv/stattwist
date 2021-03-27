import env
import tweepy
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter
from pydantic import BaseModel
from .auth import get_api_instance

class OAuthRequestTokens(BaseModel):
    access_token: str
    access_token_secret: str
    class Config:
        orm_mode: True

class TopTweetsResponse(BaseModel):
    retrieved_at: datetime
    most_retweeted_ids: List[str]
    most_liked_ids: List[str]

class TweetIdsRequest(BaseModel):
    access_token: str
    access_token_secret: str
    most_liked_ids: str
    most_retweeted_ids: str
    class Config:
        orm_mode: True

class TweetCardsResponse(BaseModel):
    most_liked_cards: List[str]
    most_retweeted_cards: List[str]

router = APIRouter()

@router.post('/dashboard/load', response_model=TopTweetsResponse)
async def load_top_tweets(tokens: OAuthRequestTokens):
    #sample_id = "1359180950672977920"
    api = get_api_instance(tokens.access_token, tokens.access_token_secret)
    date_one_year_ago = datetime.now() - timedelta(days=365)
    top_retweets = [{'id_str':None, 'retweets':-1}]*6
    top_likes = [{'id_str':None, 'likes':-1}]*6
    for status in tweepy.Cursor(api.user_timeline).items():
        if status.retweeted or status.text[:4] == 'RT @':
            continue
        if status.created_at < date_one_year_ago:
            break
        if status.retweet_count > top_retweets[0]['retweets']:
            top_retweets[0] = {'id_str':status.id_str, 'retweets':status.retweet_count}
            top_retweets.sort(key=lambda x:x['retweets'])
        if status.favorite_count > top_likes[0]['likes']:
            top_likes[0] = {'id_str':status.id_str, 'likes':status.favorite_count}
            top_likes.sort(key=lambda x:x['likes'])
    most_retweeted_ids = [x['id_str'] for x in top_retweets]
    most_liked_ids = [x['id_str'] for x in top_likes]
    return {
        'retrieved_at':datetime.now(),
        'most_retweeted_ids':most_retweeted_ids,
        'most_liked_ids':most_liked_ids
    }

@router.post('/dashboard/render', response_model=TweetCardsResponse)
async def load_tweets_html(req: TweetIdsRequest):
    api = get_api_instance(req.access_token, req.access_token_secret)
    most_retweeted_cards = []
    most_liked_cards = []
    for id in req.most_retweeted_ids.replace('[^\w,]+','').split(','):
        most_retweeted_cards.append(api.get_oembed(url="https://twitter.com/{}/status/{}".format(api.me().screen_name, id))['html'])
    for id in req.most_liked_ids.replace('[^\w,]+','').split(','):
        most_liked_cards.append(api.get_oembed(url="https://twitter.com/{}/status/{}".format(api.me().screen_name, id))['html'])
    return {
        'most_retweeted_cards':most_retweeted_cards,
        'most_liked_cards':most_liked_cards
    }
