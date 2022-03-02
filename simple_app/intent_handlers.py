## intent handlers

def userHelpIntentHandler(message):
    textResponse = """
    <指令集>
    幫助: !help
    葛格今天煮什麼: !cook
    小寶貝美甲預約: !nailbook
    腳踏車站搜尋: !youbike
    """
    return {
        "type": 'text',
        "text": f'葛格幫:{textResponse}'
    }


