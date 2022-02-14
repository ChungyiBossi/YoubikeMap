
from flask import Flask, render_template, request, Response, Blueprint
from markupsafe import escape
from .models import search_hint

simple_route = Blueprint("simple_route", __name__)

@simple_route.route("/")
def home_page():
    return render_template("home.html")

@simple_route.route("/add/rawdata", methods=["POST"])  ## further, use form to update
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