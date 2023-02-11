from ..models.line_apis import (
    getUserProfile,
    sendReplyMessage,
    sendPushMessage,
    getImageContent
)
from simple_app.models.intent_handlers import *
from simple_app.postgreSQL.session import create_sql_scoped_session
from simple_app.postgreSQL.tables import LineUser
from flask import current_app
import re
import logging

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
        'keywords': ["跟我聊聊", "你知道什麼是", "你知道", "聊聊"],
        'whole_sentence': True,
        'handler': openaiHandler
    },
    "生成圖片": {
        'keywords': ["生成圖片", "一張圖包含"],
        'whole_sentence': False,
        'handler': openaiImageCreateHandler
    }
}


def simpleIntentClassifier(userId, rawMsg):

    for intent_type, intent_info in intent_map.items():
        keywords = intent_info['keywords']
        if keywords:
            regex_pattern = keywords_to_regex(keywords)
            handler = intent_info['handler']
            matched_kw, message = \
                match_intent_keywords_and_msg(rawMsg, regex_pattern)
            if matched_kw:
                return {
                    'userId': userId,
                    'intentHandler': handler,
                    'intentType': intent_type,
                    'intentMessage': matched_kw + message
                    if intent_info['whole_sentence'] else message
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
    logging.warn(jsonData)
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
                # TODO: 需要一個類似flow概念的接續方法。
                # 假設收到地點，代表要找其鄰近的餐廳/咖啡廳/電影院
                latlng = msg_body['latitude'], msg_body['longitude']
                response = findPlaceHandler(userId, latlng)
                sendReplyMessage(replyToken, response)
                # sendPushMessage(userId, response)  # debug, 不透過webhook
            elif msg_body['type'] == 'image':
                # TODO:收到圖片的處理
                getImageContent(msg_body)
                pass

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


def keywords_to_regex(keywords):
    kws = "|".join(keywords)
    return re.compile(f"({kws})+[ ]*([^ ]*)")


def match_intent_keywords_and_msg(user_msg, regex_pattern):
    # TODO:全半形控制
    result = re.search(regex_pattern, user_msg)
    if result:
        groups = result.groups()
        return groups[0], "".join(groups[1:])
    else:
        return "", user_msg
