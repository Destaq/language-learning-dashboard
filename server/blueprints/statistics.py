from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.log import Log
from models.goal_message import GoalMessage
from dateutil import parser
import datetime

statistics_bp = Blueprint("statistic", __name__)


# NOTE: updating user statistics occurs from withing the `log` blueprint (a bit counterintuitively, update?)

@statistics_bp.route("/fetch-statistics", methods=["GET"])
def fetch_statistics():
    # this returns interesting tidbits: characters read, chapters read, books read, # of shows + movies watched, all-time study hours, vocab size
    # the user levels are currently hardcoded, may be changed later, but for now simple like this
    user = User.query.filter_by(id=1).first()
    total_hours = sum(
        [log.length / 60 for log in Log.query.filter_by(user_id=user.id).all()]
    )

    first_log_date = (
        Log.query.filter_by(user_id=user.id).order_by(Log.date.asc()).first().date
    )

    # calculate days since first log
    today = datetime.datetime.now()
    days_since_first_log = (today - first_log_date).days + 1

    goals_completed = GoalMessage.query.filter_by(user_id=user.id, completed=True).count()


    return jsonify(
        statistics=[
            {"name": "Total Study Time", "value": round(total_hours, 2)},
            {"name": "Daily Average", "value": round(total_hours / days_since_first_log, 2)},
            {"name": "Vocab Size (Words)", "value": user.vocab_size},
            {"name": "Characters Read", "value": user.characters_read},
            {"name": "Chapters Read", "value": user.chapters_read},
            {"name": "Books Read", "value": user.books_read},
            {"name": "Episodes/Movies Watched", "value": user.shows_watched},
            {"name": "Goals Completed", "value": goals_completed},
        ],
        character_vocab_size=user.character_size,
        word_vocab_size=user.vocab_size,
    )
