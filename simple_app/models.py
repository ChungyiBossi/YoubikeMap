from .line_apis import (
    getUserProfile,
    sendReplyMessage,
    sendPushMessage
)
from .intent_handlers import *


# 測試用，已改用line bot做設定
def generateMessageBody(message):
    if message == "!help":
        return [userHelpIntentHandler(message)]
    else:
        return [{
            "type": 'text',
            "text": f'葛格回覆說:{message}'
        }]


def handleLineMessage(jsonData):

    for event in jsonData['events']:
        userId = event["source"]["userId"]  # 推送到前端去需要userId
        replyToken = event["replyToken"]

        profile = getUserProfile(userId).json()
        if event['type'] == 'message':
            message = event["message"]["text"]  # 使用者端提問文字串內容
            sendReplyMessage(replyToken, generateMessageBody(message))
            sendPushMessage(userId, generateMessageBody(message))  # debug

        if event['type'] == 'follow':
            userName = profile.get('displayName', '您')
            greeting = f'歡迎 {userName} 的加入 這是一個葛格煮平台!!!'
            sendReplyMessage(replyToken, generateMessageBody(greeting))

    return '訊息處理結束'



