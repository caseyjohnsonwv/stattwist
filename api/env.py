from dotenv import load_dotenv
load_dotenv()

from os import getenv
API_HOST = getenv('API_HOST') or "localhost"
API_PORT = getenv('API_PORT') or "5000"
TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = getenv('TWITTER_API_SECRET')
TWITTER_CALLBACK_URL = getenv('TWITTER_CALLBACK_URL') or "http://localhost:8080/auth/callback"
UI_HOST = getenv("UI_HOST") or "http://localhost:8080"
