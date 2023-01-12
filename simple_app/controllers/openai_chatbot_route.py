from flask import (
    jsonify,
    Blueprint
)
from simple_app.models import question_and_answer

openai_chatbot = Blueprint("openai_chatbot", __name__)


@openai_chatbot.route("/qa_openai/<msg>")
def answer_questions(msg=""):

    response = question_and_answer(msg)
    return response
