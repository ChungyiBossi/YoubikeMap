from flask import (
    render_template,
    Blueprint
)
from simple_app.models import question_and_answer, chat, text_to_image

teachable_machine = Blueprint("teachable_machine", __name__)


@teachable_machine.route("/tm/")
def render_teachable_machine():
    # 需要https才能正常運作（chrome）
    return render_template("online_tm_page.html")
