
from flask import (
    render_template,
    abort, jsonify,
    request,
    Blueprint
)
from simple_app.models import webSocketEmit
from .intent_classifier import handleLineMessage

simple_route = Blueprint("simple_route", __name__)


@simple_route.route("/")
def test_smoke():
    return "Chung Yi's website is hosting...."


@simple_route.route("/smokeTest")
def test_smoke():
    return "No smoke here"


@simple_route.route("/google_map", methods=["GET"])
def google_map_sample():
    return render_template("google_map.html")


@simple_route.route('/line/message/webhook', methods=["POST"])
def lineWebhook():
    # requested by a line webhook event, 再透過push event 傳遞至channel再至client
    jsonData = request.get_json()
    handleLineMessage(jsonData)
    return '訊息處理結束'


@simple_route.route("/websocket", methods=['GET', 'POST'])
def upload():
    # TODO: logging
    # update data through http request, handle it by websocket
    if not request.json:
        print("Data is not json format")
        abort(400)
    print("Data: ", request.json)
    d = request.json.get("data", 0)
    webSocketEmit(d)  # 傳遞給各個client端
    return jsonify(
        {"response": "ok"}
    )


@simple_route.route("/webSocketTest")
def webSocketTest():
    # webSocket test client
    return render_template('webSocketTest.html', async_mode='eventlet')
