from flask import current_app
from collections import defaultdict
from .line_msg_generator import *
from .openai_api import chat, text_to_image

memory = defaultdict(lambda: dict())  # local memory


def updateMemory(userId, **kwargs):
    for k, v in kwargs.items():
        memory[userId][k] = v


def findPlaceHandler(userId, latlng):
    message = memory[userId].get('search_input_message', "restaurant")
    result = current_app.google_client.find_place(message, latlng)
    if result['status'] == "OK":
        candidate = result['candidates'][0]
        print(f"Find Place: *{candidate}*")
        return [
            {
                "type": "text",
                "text": f"找到了！"
            },
            {
                "type": "location",
                "title": candidate['name'],
                "address": candidate['formatted_address'],
                "latitude": candidate['geometry']['location']['lat'],
                "longitude": candidate['geometry']['location']['lng']
            }
        ]
    else:
        return [
            {
                "type": "text",
                "text": f"我找不到此地點附近的 *{message}*, 要不要換一個方式說呢?"
            }
        ]


def requestLocationHandler(userId, message):
    if message:
        updateMemory(userId, search_input_message=message)
        print(f"Find *{message}*, request User Location")
        return [{
            "type": "text",
            "text": f"請選擇您欲查詢 {message} 的位置",
            "quickReply": {
                "items": [
                    location_action('選擇欲查詢的地點')
                ]
            }
        }]
    else:
        return [{
            "type": "text",
            "text": f"要查什麼呢?",
            "quickReply": {
                "items": [
                    message_action("餐廳", "幫我找 餐廳"),
                    message_action("咖啡廳", "幫我找 咖啡廳"),
                    message_action("電影院", "幫我找 電影院")
                ]
            }
        }]


def defaultHandler(userId, message):
    return [{
        "type": 'text',
        "text": f'請您再更詳細描述問題唷！'
    }]


def userHelpIntentHandler(userId, message):
    textResponse = """
    幫助: !help
    找地點: !find 餐廳/咖啡廳/電影院
    """
    return [{
        "type": 'text',
        "text": f'葛格回覆說:{textResponse}'
    }]


def carActionHandler(userId, message):
    if message in ["順時針轉", "順轉", "順時針"]:  # some kind of entity infomation
        current_app.extensions['socketio'].emit(
            'car_rotate', {'rotationSide': 1}, namespace="/")
    elif message in ["逆時針轉", "逆轉", "逆時針"]:
        current_app.extensions['socketio'].emit(
            'car_rotate', {'rotationSide': -1}, namespace="/")
    return [{
        "type": 'text',
        "text": f'車輛控制:{message}'
    }]


def openaiHandler(userId, message):
    # TODO: cut the sentences for better presentation

    return [{
        "type": 'text',
        "text": chat(message).strip()
    }]


def openaiImageCreateHandler(usrId, message):
    return [image_message(text_to_image(message).strip())]
