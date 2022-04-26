
from flask import (
    render_template, 
    abort, jsonify,
    current_app,
    request, 
    Blueprint
)
from flask_socketio import (
    send, emit
)
from markupsafe import escape
from .models import handleLineMessage

simple_route = Blueprint("simple_route", __name__)

@simple_route.route("/smokeTest")
def test_smoke():
    return "No smoke here"


@simple_route.route("/google_map", methods=["GET"])
def google_map_sample():
    return render_template("google_map.html")


# request by a line webhook event, 再透過push event 傳遞至channle再至client
@simple_route.route('/line/message/webook', methods=["POST"])
def lineWebhook():
    jsonData = request.get_json()
    handleLineMessage(jsonData)
    return '訊息處理結束'

# TODO: logging
# update data through http request, handle it by websocket 
@simple_route.route("/websocket", methods=['GET', 'POST'])
def upload():
    if not request.json:
        print("Data is not json format")
        abort(400)
    print("Data: ", request.json)
    d = request.json.get("data", 0)
    webSocketEmit(d)
    return jsonify(
        {"response": "ok"}
    )

# webSocket test client 
@simple_route.route("/webSocketTest")
def webSocketTest():
    return render_template('webSocketTest.html', async_mode='eventlet')

# Move to model.py
def webSocketEmit(data):
    # 回傳給前端
    emit('car_rotate', {'data': data})
    print("Socket IO emit finished.")
    