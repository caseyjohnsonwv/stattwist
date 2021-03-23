import env
import tweepy
from fastapi import APIRouter
from pydantic import BaseModel

class OAuthInitiatedResponse(BaseModel):
    request_token: dict
    redirect_url: str
    class Config:
        orm_mode: True

class OAuthFrontendCallback(BaseModel):
    request_token: dict
    verifier: str
    class Config:
        orm_mode: True

class OAuthCompletedResponse(BaseModel):
    access_token: str
    access_token_secret: str
    class Config:
        orm_mode: True

router = APIRouter()

@router.get('/auth', response_model=OAuthInitiatedResponse)
def initiate_oauth():
    auth = tweepy.OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET, env.TWITTER_CALLBACK_URL)
    redirect_url = auth.get_authorization_url()
    request_token = auth.request_token
    return {'request_token':request_token, 'redirect_url':redirect_url}

@router.post('/auth/callback', response_model=OAuthCompletedResponse)
def complete_oauth(data: OAuthFrontendCallback):
    auth = tweepy.OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET)
    auth.request_token = data.request_token
    auth.get_access_token(data.verifier)
    return {'access_token':auth.access_token, 'access_token_secret':auth.access_token_secret}

def get_api_instance(access_token, access_token_secret):
    auth = tweepy.OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET)
    auth.access_token = access_token
    auth.access_token_secret = access_token_secret
    api = tweepy.API(auth)
    return api
