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
