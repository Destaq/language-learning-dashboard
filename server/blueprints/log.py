from flask import Blueprint, request, jsonify
from extensions import db
from models.log import Log
from models.user import User

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


@log_bp.route("/upload-log-file", methods=["POST", "OPTIONS"])
def upload_log_file():
    file = request.files["file"]
    parse_and_use_file(file)
    return jsonify(success=True)

@log_bp.route("/possible-daily-actions", methods=["GET"])
def action_templater():
    # some action templates on the left as cards that fill out the custom log area
    action_user = User.query.filter_by(id=1).first()  # NOTE: hardcoded for prototype
    return jsonify(actions=action_user.get_actions())


# HELPER FUNCTIONS - READ ANKI + PLECO TO GET HISTORY
# ANKI OR PLECO OR SCREEN TIME CUSTOM FILE
def parse_and_use_file(file):
    # parse the file (file.read())
    # use the data to create a new log
    # NOTE: custom file upload is for VOCAB TRACKING ONLY
    # to track time, upload screen time to the custom log
    pass
