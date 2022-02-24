# 讀取ubike線上即時資訊
# 建立一個自訂函數 讀取ubike資料,透過傳遞進來區域參數 找出相對資訊
import requests as re  # as 定義一個別名alias Name
from flask import current_app
import json


def search_hint(currentWord):
    hint_list = ["信義區", "大同區", "中山區", "士林區", "中正區", "萬華區",
                 "大安區", "文山區", "內湖區", "松山區", "南港區", "淡水區", "天母區"]
    result = ",".join([h for h in hint_list if currentWord in h])
    return result


def receiveLineMessage(jsonData):

    for event in jsonData['events']:
        userType = event["source"]["type"]
        userId = event["source"]["userId"]  # 推送到前端去需要userId

        # 進行訊息(message or follow)分支控制流成
        if event['type'] == 'message':

            # 取出前端Line送出文字訊息
            msgType = event["message"]["type"]  # 確定是一個text類型
            message = event["message"]["text"]  # 使用者端提問文字串內容
            sendPushMessage(userId, message)

        # 新增為好友的解除
        if event['type'] == 'follow':
            greeting = '歡迎你 的加入 這是一個物聯網自然語言服務平台!!!'
            sendPushMessage(userId, greeting)

    return '訊息處理結束'


def sendPushMessage(userId, message):
    # 1.需要Web Client一個Request物件(或者功能)
    # 2 send push message網址
    pushURL = 'https://api.line.me/v2/bot/message/push'
    lineChannelAccessToken = current_app.config['LINE_CHANNEL_ACCESS_TOKEN']
    # 設定dict 設定Content-Type and Authorization
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {lineChannelAccessToken}"
    }
    body = {
        "to": userId,
        "messages": [
            {
                "type": 'text',
                "text": f'我說:{message}'
            }
        ]
    }
    re.post(pushURL, headers=headers, data=json.dumps(body))
