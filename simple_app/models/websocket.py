from flask import current_app


def webSocketEmit(data):
    # 回傳給前端
    current_app.extensions['socketio'].emit(
        'http_event', {'data': data}, namespace="/")
    print("Socket IO emit finished.")
