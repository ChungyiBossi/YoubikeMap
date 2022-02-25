import os
DEBUG = True
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_REPLY_API = 'https://api.line.me/v2/bot/message/reply'
LINE_PUSH_API  = 'https://api.line.me/v2/bot/message/push'