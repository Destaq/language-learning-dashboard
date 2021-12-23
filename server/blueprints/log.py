from flask import Blueprint, request, jsonify
from extensions import db
from models.log import Log
from models.user import User
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

log_bp = Blueprint("log", __name__)


@log_bp.route("/submit-custom-log", methods=["POST"])
def submit_custom_log():
    # get the data from the request
    data = request.get_json()

    # create a new log
    log = Log(
        title=data["title"],
        user_id=1,  # NOTE: hardcoded for prototype
        length=data["length"],
        type=data["type"],
        language="zh",  # NOTE: hardcoded for prototype
    )
    log.date = data["date"]

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


@log_bp.route("/hours-by-period", methods=["GET"])
def hours_by_period():
    # get period and starting_date from request
    period = request.args.get("period")
    # request.args starting_date is in the format: YYYY-MM-DD
    starting_date = parse(request.args.get("starting_date"))
    information = {
        "Reading": [],
        "Writing": [],
        "Listening": [],
        "Speaking": [],
        "Other": [],
    }

    if period == "week":
        ending_date = relativedelta(days=7) + starting_date
        periods = 7
    elif period == "month":
        ending_date = relativedelta(months=1) + starting_date
        periods = (ending_date - starting_date).days
    elif period == "year":
        ending_date = relativedelta(years=1) + starting_date
        periods = 12

    for i in range(periods):
        information["Reading"].append(0)
        information["Writing"].append(0)
        information["Listening"].append(0)
        information["Speaking"].append(0)
        information["Other"].append(0)

    # get the logs within the two time periods
    logs = Log.query.filter(Log.date >= starting_date, Log.date < ending_date).all()

    dates = []

    if periods != 12:
        # now fill out the information container, with each list item representing a consecutive date
        # we are going day-by-day since it is less than or equal to one month in length
        for log in logs:
            if log.type == "Reading":
                information["Reading"][(log.date - starting_date).days] += (
                    log.length / 60
                )
            elif log.type == "Writing":
                information["Writing"][(log.date - starting_date).days] += (
                    log.length / 60
                )
            elif log.type == "Listening":
                information["Listening"][(log.date - starting_date).days] += (
                    log.length / 60
                )
            elif log.type == "Speaking":
                information["Speaking"][(log.date - starting_date).days] += (
                    log.length / 60
                )
            else:
                information["Other"][(log.date - starting_date).days] += log.length / 60

        for i in range(periods):
            that_date = starting_date + relativedelta(days=i)
            # format in the format: MM-DD
            dates.append(that_date.strftime("%m-%d"))

    else:
        # this is in years format, so we will divide the data up into months
        for log in logs:
            # get the month that the log was written
            month = log.date.month - 1
            if log.type == "Reading":
                information["Reading"][month] += log.length / 60
            elif log.type == "Writing":
                information["Writing"][month] += log.length / 60
            elif log.type == "Listening":
                information["Listening"][month] += log.length / 60
            elif log.type == "Speaking":
                information["Speaking"][month] += log.length / 60
            else:
                information["Other"][month] += log.length / 60

        for i in range(periods):
            # append the month to dates, where the month is in the format 'Jan '19', and starts at starting_date month
            dates.append(
                (starting_date + relativedelta(months=i)).strftime("%b '%y")
            )
            
    return jsonify(information=information, dates=dates)


# HELPER FUNCTIONS - READ ANKI + PLECO TO GET HISTORY
# ANKI OR PLECO OR SCREEN TIME CUSTOM FILE
def parse_and_use_file(file):
    # parse the file (file.read())
    # use the data to create a new log
    # NOTE: custom file upload is for VOCAB TRACKING ONLY
    # to track time, upload screen time to the custom log
    pass
