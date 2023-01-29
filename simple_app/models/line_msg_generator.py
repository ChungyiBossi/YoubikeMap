def location_action(label):
    return {
        "type": "action",
        "action": {
            "type": "location",
            "label": label
        }
    }


def message_action(label, text):
    return {
        "type": "action",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        }
    }


def image_message(img_url):
    # https://developers.line.biz/en/reference/messaging-api/#image-message
    return {
        "type": "image",
        "originalContentUrl": img_url,
        "previewImageUrl": img_url
    }
