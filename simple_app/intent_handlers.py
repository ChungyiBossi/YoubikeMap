from flask import current_app
from collections import defaultdict
memory = defaultdict(lambda: dict())

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
                    {
                        "type": "action",
                        "action": {
                            "type": "location",
                            "label": "選擇欲查詢的地點"
                        }
                    }
                ]
            }
        }]
    else:
        return [{
            "type": "text",
            "text": f"要查什麼呢?",
            "quickReply": {
                "items": [
                    {
                        "type": "action",
                        "action": {
                            "type": "message",
                            "label": "餐廳",
                            "text": "找 餐廳"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type": "message",
                            "label": "咖啡廳",
                            "text": "找 咖啡廳"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type": "message",
                            "label": "電影院",
                            "text": "找 電影院"
                        }
                    }
                    
                ]
            }
        }]


def defaultHandler(userId, message):
    return [{
        "type": 'text',
        "text": f'葛格回覆說:{message}'
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
    if message in ["順時針轉", "順轉"]:
        current_app.socketio.emit('status_response', {'rotationSide': 1}, namespace="/")
    elif message in ["逆時針轉", "逆轉"]:
        current_app.socketio.emit('status_response', {'rotationSide': -1}, namespace="/")
    return [{
        "type": 'text',
        "text": f'車輛控制:{message}'
    }]
