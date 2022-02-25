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
        userId = event["source"]["userId"]  # 推送到前端去需要userId
        replyToken = event["replyToken"]

        profile = getUserProfile(userId).json()
        # 進行訊息(message or follow)分支控制流成
        if event['type'] == 'message':
            message = event["message"]["text"]  # 使用者端提問文字串內容
            sendReplyMessage(replyToken, message)

        # 新增為好友的解除
        if event['type'] == 'follow':
            userName = profile.get('displayName', '您')
            greeting = f'歡迎 {userName} 的加入 這是一個物聯網自然語言服務平台!!!'
            sendReplyMessage(replyToken, greeting)

    return '訊息處理結束'


def getLineReqHeader():
    lineChannelAccessToken = current_app.config['LINE_CHANNEL_ACCESS_TOKEN']
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {lineChannelAccessToken}"
    }


def getUserProfile(userId: str):

    return re.get(current_app.config['LINE_PROFILE_API']+userId, headers=getLineReqHeader())


def sendReplyMessage(replyToken, message):
    replyUrl = current_app.config['LINE_REPLY_API']
    body = {
        "replyToken": replyToken,
        "messages": [
            {
                "type": 'text',
                "text": f'葛格回覆說:{message}'
            }
        ]
    }
    resp = re.post(replyUrl, headers=getLineReqHeader(), data=json.dumps(body))
    return resp.status_code


def sendPushMessage(userId, message):
    pushURL = current_app.config['LINE_PUSH_API']
    body = {
        "to": userId,
        "messages": [
            {
                "type": 'text',
                "text": f'葛格推播說:{message}'
            }
        ]
    }
    resp = re.post(pushURL, headers=getLineReqHeader(), data=json.dumps(body))
    return resp.status_code
