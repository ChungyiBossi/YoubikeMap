from ..models.line_apis import (
    getUserProfile,
    sendReplyMessage,
    sendPushMessage
)
from simple_app.models.intent_handlers import *
from simple_app.postgreSQL.session import create_sql_scoped_session
from simple_app.postgreSQL.tables import LineUser
from flask import current_app

intent_map = {
    # intent type: keywords
    "主頁選單": {
        'keywords': ['!help', '!幫助', '!主頁'],
        'whole_sentence': False,
        'handler': userHelpIntentHandler
    },
    "找地點": {
        'keywords': ["幫我找", "幫忙找", "!找", "!find"],
        'whole_sentence': False,
        'handler': requestLocationHandler
    },
    "default": {
        'keywords': [],
        'whole_sentence': False,
        'handler': defaultHandler
    },
    "車輛控制": {
        'keywords': ["!車輛控制", "!Arduino"],
        'whole_sentence': False,
        'handler': carActionHandler
    },
    "聊天": {
        'keywords': ["跟我聊聊", "你知道什麼是", "你知道"],
        'whole_sentence': True,
        'handler': openaiHandler
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

    print(
        f"Parts: *{parts}*, Intent word: *{intent_word}*, Intent Msg: *{intent_msg}*")

    for intent_type, intent_info in intent_map.items():
        keywords, handler = intent_info['keywords'], intent_info['handler']
        for k in keywords:
            if k in intent_word:  # 用起頭字判定意圖
                return {
                    'userId': userId,
                    'intentHandler': handler,
                    'intentType': intent_type,
                    'intentMessage': intent_word + intent_msg
                    if intent_info['whole_sentence'] else intent_msg
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
    current_app.extensions['socketio'].emit(
        'msg_receive', {'intent': type, 'text': msg}, namespace="/")
    return handler(userId, msg)


def handleLineMessage(jsonData):
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
                response = getIntentResponse(
                    **simpleIntentClassifier(userId, message))
                sendReplyMessage(replyToken, response)
                # sendPushMessage(userId, response)  # debug
            elif msg_body['type'] == 'location':
                # 假設收到地點，代表要找其鄰近的餐廳/咖啡廳/電影院
                latlng = msg_body['latitude'], msg_body['longitude']
                response = findPlaceHandler(userId, latlng)
                sendReplyMessage(replyToken, response)
                # sendPushMessage(userId, response)  # debug, 不透過webhook

        elif event['type'] == 'follow':
            userName = profile.get('displayName', '您')
            greeting = f'歡迎 {userName} 的加入 這是一個葛格煮平台!!!'
            sendReplyMessage(replyToken, defaultHandler(userId, greeting))

    # merge db data
    if current_app.config.get("ENABLE_POSTGRESQL"):
        session = create_sql_scoped_session(current_app.db_engine)
        for uid, d in update_line_user_data.items():
            table = update_line_user_data[uid]['type']
            name = update_line_user_data[uid]['info'].get('displayName', "")
            session.merge(table(uid, name))
        session.commit()
    return '訊息處理結束'
