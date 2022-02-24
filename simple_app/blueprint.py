
from flask import Flask, render_template, request, Response, Blueprint
from markupsafe import escape
from .models import search_hint, receiveLineMessage

simple_route = Blueprint("simple_route", __name__)


@simple_route.route("/")
def home_page():
    return render_template("home.html")


@simple_route.route("/smokeTest")
def test_smoke():
    return "No smoke here"


@simple_route.route("/search_youbike", methods=["GET"])
def search_youbike():
    return render_template("search_youbike.html")


@simple_route.route("/search_hint/<query>", methods=["GET"])
def search_hint_page(query):
    return search_hint(escape(query))


@simple_route.route("/google_map", methods=["GET"])
def google_map_sample():
    return render_template("google_map.html")


# request by a line webhook event, 再透過push event 傳遞至channle再至client
@simple_route.route('/line/message/webook', methods=["POST"])
def receiveMessage():
    jsonData = request.get_json()
    receiveLineMessage(jsonData)
    return '訊息處理結束'
