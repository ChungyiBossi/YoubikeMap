from .line_apis import (
    getUserProfile,
    sendReplyMessage,
    sendPushMessage
)
from .intent_handlers import *
from .postgreSQL.session import create_sql_scoped_session
from .postgreSQL.tables import LineUser
from flask import current_app


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
    session = create_sql_scoped_session(current_app.db_engine)
    update_line_user_data = dict()

    for event in jsonData['events']:
        userId = event["source"]["userId"]  # 推送到前端去需要userId
        profile = getUserProfile(userId).json()
        update_line_user_data[userId] = {
            'type': LineUser,
            'info': profile
        }
        replyToken = event["replyToken"]
        if event['type'] == 'message':
            message = event["message"]["text"]  # 使用者端提問文字串內容
            sendReplyMessage(replyToken, generateMessageBody(message))
            sendPushMessage(userId, generateMessageBody(message))  # debug

        if event['type'] == 'follow':
            userName = profile.get('displayName', '您')
            greeting = f'歡迎 {userName} 的加入 這是一個葛格煮平台!!!'
            sendReplyMessage(replyToken, generateMessageBody(greeting))

    # merge db data
    for uid, d in update_line_user_data.items():
        table = update_line_user_data[uid]['type']
        name =  update_line_user_data[uid]['info'].get('displayName', "")
        session.merge(table(uid, name))
    session.commit()
    return '訊息處理結束'



