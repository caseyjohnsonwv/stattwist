from dotenv import load_dotenv
load_dotenv()

from os import getenv
API_HOST = getenv('API_HOST')
API_PORT = getenv('API_PORT')
TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = getenv('TWITTER_API_SECRET')
TWITTER_CALLBACK_URL = getenv('TWITTER_CALLBACK_URL')
UI_HOST = getenv("UI_HOST")
UI_PORT = getenv("UI_PORT")
