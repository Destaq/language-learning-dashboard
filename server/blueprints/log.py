from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.log import Log

log_bp = Blueprint("log", __name__)


@log_bp.route("/submit-custom-log", methods=["POST", "OPTIONS"])
def submit_custom_log():
    # get the data from the request
    data = request.get_json()

    # create a new log
    log = Log(
        text=data["text"],
        title=data["title"],
        user_id=1,  # NOTE: hardcoded for prototype
        length=data["length"],
        type=data["type"],
        language="zh",  # NOTE: hardcoded for prototype
    )

    # add the log to the database
    db.session.add(log)
    db.session.commit()

    # return the log
    return jsonify(success=True)
