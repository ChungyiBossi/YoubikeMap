
from flask import Flask, render_template, request, Response, Blueprint
from markupsafe import escape
from .models import search_hint, receiveLineMessage

simple_route = Blueprint("simple_route", __name__)

@simple_route.route("/")
def home_page():
    return render_template("home.html")

# further, use form to update
@simple_route.route("/add/rawdata", methods=["POST"])
def add_rawdata():
    data = request.get_json()
    return render_template("add_rawdata.html", data=data)


@simple_route.route("/search_youbike", methods=["GET"])
def search_youbike():
    return render_template("search_youbike.html")


@simple_route.route("/google_map", methods=["GET"])
def google_map_sample():
    return render_template("google_map.html")


@simple_route.route("/search_hint/<query>", methods=["GET"])
def search_hint_page(query):
    return search_hint(escape(query))

@simple_route.route('/line/message/webook', methods=["POST"])   # request by a line webhook event, 再透過push event 傳遞至channle再至client
def receiveMessage():
    jsonData = request.get_json()
    receiveLineMessage(jsonData)
    return '訊息處理結束'
