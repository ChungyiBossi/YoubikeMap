import requests as re
import json
from flask import current_app


# TODO: reply with Line SDK
# https://github.com/line/line-bot-sdk-python
# from linebot import LineBotApi
# def generateLineBotReplier():
#     return LineBotApi(current_app.config['LINE_CHANNEL_ACCESS_TOKEN'])



## Reply with RESTful api
def getLineReqHeader():
    lineChannelAccessToken = current_app.config['LINE_CHANNEL_ACCESS_TOKEN']
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {lineChannelAccessToken}"
    }

def getUserProfile(userId: str):
    
    return re.get(current_app.config['LINE_PROFILE_API']+userId, headers=getLineReqHeader())


def sendReplyMessage(replyToken, messageBody):
    replyUrl = current_app.config['LINE_REPLY_API']
    body = {
        "replyToken": replyToken,
        "messages": messageBody
    }
    resp = re.post(replyUrl, headers=getLineReqHeader(), data=json.dumps(body))
    return resp.status_code


def sendPushMessage(userId, messageBody):
    pushURL = current_app.config['LINE_PUSH_API']
    body = {
        "to": userId,
        "messages": messageBody
    }
    resp = re.post(pushURL, headers=getLineReqHeader(), data=json.dumps(body))
    return resp.status_code
