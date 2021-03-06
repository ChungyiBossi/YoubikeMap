from curses import use_default_colors
from simple_app.line_apis import (
    getUserProfile,
    sendReplyMessage,
    sendPushMessage
)
from simple_app.intent_handlers import *
from simple_app.postgreSQL.session import create_sql_scoped_session
from simple_app.postgreSQL.tables import LineUser
from flask import current_app

intent_map = {
    # intent type: keywords
    "主頁選單": {
        'keywords': ['!help', '!幫助', '!主頁'],
        'handler': userHelpIntentHandler
    },
    "找地點": {
        'keywords': ["幫我找", "幫找", "找", "!find"],
        'handler': requestLocationHandler
    },
    "default": {
        'keywords': [],
        'handler': defaultHandler
    },
    "車輛控制": {
        'keywords': ["車輛控制", "控車", "Arduino"],
        'handler': carActionHandler
    }
}


def simpleIntentClassifier(userId, rawMsg):
    ## TODO: NER
    parts = rawMsg.split()

    if len(parts) >= 2:
        # 合併後面的訊息
        intent_word, intent_msg = parts[0], "".join(parts[1:])
        # TODO: TRUELY Intent classifier
    else:
        intent_word, intent_msg = parts[0], ""
    
    print(f"Parts: *{parts}*, Intent: *{intent_word}*, Intent Msg: *{intent_msg}*")

    for intent_type, intent_info in intent_map.items():
        keywords, handler = intent_info['keywords'], intent_info['handler']
        for k in keywords:
            if k in intent_word:  # 用起頭字判定意圖
                return {
                    'userId': userId,
                    'intentHandler': handler,
                    'intentType': intent_type,
                    'intentMessage': intent_msg
                }
    return {
        'userId': userId,
        'intentHandler': defaultHandler,
        'intentType': "default",
        'intentMessage': rawMsg
    } 


def getIntentResponse(**kwargs):
    userId = kwargs['userId']
    handler = kwargs['intentHandler']
    type = kwargs['intentType']
    msg = kwargs['intentMessage']
    current_app.extensions['socketio'].emit('msg_receive', {'intent': type, 'text': msg}, namespace="/")    
    return handler(userId, msg)


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
            msg_body = event['message']

            if msg_body['type'] == 'text':
                message = msg_body["text"]  # 使用者端提問文字串內容
                response = getIntentResponse(**simpleIntentClassifier(userId, message))
                sendReplyMessage(replyToken, response)
                # sendPushMessage(userId, response)  # debug
            elif msg_body['type'] == 'location':
                latlng = msg_body['latitude'], msg_body['longitude']
                response = findPlaceHandler(userId, latlng)
                sendReplyMessage(replyToken, response)
                # sendPushMessage(userId, response)  # debug, 不透過webhook

        elif event['type'] == 'follow':
            userName = profile.get('displayName', '您')
            greeting = f'歡迎 {userName} 的加入 這是一個葛格煮平台!!!'
            sendReplyMessage(replyToken, defaultHandler(userId, greeting))

    # merge db data
    for uid, d in update_line_user_data.items():
        table = update_line_user_data[uid]['type']
        name = update_line_user_data[uid]['info'].get('displayName', "")
        session.merge(table(uid, name))
    session.commit()
    return '訊息處理結束'


def webSocketEmit(data):
    # 回傳給前端
    current_app.extensions['socketio'].emit('http_event', {'data': data}, namespace="/")
    print("Socket IO emit finished.")
    