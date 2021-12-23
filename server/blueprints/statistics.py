from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.log import Log

statistics_bp = Blueprint("statistic", __name__)


@statistics_bp.route("/fetch-statistics", methods=["GET"])
def fetch_statistics():
    # this returns interesting tidbits: characters read, chapters read, books read, # of shows + movies watched, all-time study hours, vocab size
    # the user levels are currently hardcoded, may be changed later, but for now simple like this
    user = User.query.filter_by(id=1).first()
    return jsonify(
        statistics=[
            {
                "name": "All-Time Study Hours",
                "value": sum(
                    [
                        log.length / 60
                        for log in Log.query.filter_by(user_id=user.id).all()
                    ]
                ),
            },
            {"name": "Vocab Size", "value": user.vocab_size},
            {"name": "Characters Read", "value": user.characters_read},
            {"name": "Chapters Read", "value": user.chapters_read},
            {"name": "Books Read", "value": user.books_read},
            {"name": "Shows/Movies Watched", "value": user.shows_watched},
        ]
    )
