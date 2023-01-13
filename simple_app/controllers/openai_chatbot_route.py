from flask import (
    jsonify,
    request,
    Blueprint
)
from simple_app.models import question_and_answer, chat

openai_chatbot = Blueprint("openai_chatbot", __name__)


@openai_chatbot.route("/openai/qa/<msg>")
def answer_questions(msg=""):
    response = question_and_answer(msg)
    return response


@openai_chatbot.route("/openai/chat/<msg>")
def chatbot(msg=""):
    response = chat(msg)
    return response
