import os
DEBUG = True
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
POSTGRESQL_DB_URL = os.environ['POSTGRESQL_DB_URL']
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
ENABLE_POSTGRESQL = os.environ['ENABLE_POSTGRESQL']
OPENAI_APIKEY = os.environ['OPENAI_APIKEY']
LINE_REPLY_API = 'https://api.line.me/v2/bot/message/reply'
LINE_PUSH_API = 'https://api.line.me/v2/bot/message/push'
LINE_PROFILE_API = 'https://api.line.me/v2/bot/profile/'
