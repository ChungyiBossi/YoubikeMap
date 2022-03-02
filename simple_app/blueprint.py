
from flask import Flask, render_template, request, Response, Blueprint
from markupsafe import escape
from .models import handleLineMessage

simple_route = Blueprint("simple_route", __name__)


@simple_route.route("/")
def home_page():
    return render_template("home.html")


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
