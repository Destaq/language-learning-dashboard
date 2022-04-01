import re, os, requests
from flask import Blueprint, request, jsonify
from extensions import db
from models.log import Log
from models.statistic import StatisticSnapshot
from models.user import User
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from isoweek import Week


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
    is_default_view = (
        request.args.get("default_view") == "true"
    )  # this is whether we are displaying type or resource

    YEAR_PERIODS = -1

    if period == "week":
        ending_date = relativedelta(days=7) + starting_date
        periods = 7
    elif period == "month":
        ending_date = relativedelta(months=1) + starting_date
        periods = (ending_date - starting_date).days
    elif period == "year":
        ending_date = relativedelta(years=1) + starting_date
        YEAR_PERIODS = Week.last_week_of_year(starting_date.year).week
        # periods = Week.last_week_of_year(
            # starting_date.year
        # ).week
        periods = (ending_date - starting_date).days  # alternative to view each day

    # get the logs within the two time periods
    logs = Log.query.filter(Log.date >= starting_date, Log.date < ending_date).all()

    if is_default_view:
        information = {
            "Reading": [],
            "Writing": [],
            "Listening": [],
            "Speaking": [],
            "Flashcards": [],
            "Other": [],
        }

        for i in range(periods):
            information["Reading"].append(0)
            information["Writing"].append(0)
            information["Listening"].append(0)
            information["Speaking"].append(0)
            information["Flashcards"].append(0)
            information["Other"].append(0)
    else:
        # information is all possible titles in the logs in the time period
        information = {}
        for log in logs:
            if log.title not in information:
                information[log.title] = [0] * periods

    dates = []

    if periods != YEAR_PERIODS:
        # now fill out the information container, with each list item representing a consecutive date
        # we are going day-by-day since it is less than or equal to one month in length
        if is_default_view:
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
                elif log.type == "Flashcards":
                    information["Flashcards"][(log.date - starting_date).days] += (
                        log.length / 60
                    )
                else:
                    information["Other"][(log.date - starting_date).days] += (
                        log.length / 60
                    )
        else:
            for log in logs:
                information[log.title][(log.date - starting_date).days] += (
                    log.length / 60
                )

        for i in range(periods):
            that_date = starting_date + relativedelta(days=i)
            # format in the format: MM-DD
            dates.append(that_date.strftime("%m-%d"))

    else:
        # this is in years format, so we will divide the data up into weeks
        for log in logs:
            # create a new datetime object for January 1st, current year
            that_date = parse(f"{log.date.year}-01-01")
            
            # get elapsed weeks between then and the log
            week = (log.date - that_date).days // 7


            if is_default_view:
                if log.type == "Reading":
                    information["Reading"][week] += log.length / 60
                elif log.type == "Writing":
                    information["Writing"][week] += log.length / 60
                elif log.type == "Listening":
                    information["Listening"][week] += log.length / 60
                elif log.type == "Speaking":
                    information["Speaking"][week] += log.length / 60
                elif log.type == "Flashcards":
                    information["Flashcards"][week] += log.length / 60
                else:
                    information["Other"][week] += log.length / 60
            else:
                information[log.title][week] += log.length / 60

        for i in range(periods):
            # append the week to dates, in the form of MM-DD
            that_date = starting_date + relativedelta(weeks=i)
            dates.append(that_date.strftime("%m-%d"))
            # dates.append((starting_date + relativedelta(months=i)).strftime("%b '%y"))

    for (key, value) in information.items():
        information[key] = [round(x, 3) for x in value]

    return jsonify(information=information, dates=dates)


@log_bp.route("/historical-breakdown", methods=["GET"])
def historical_breakdown():
    period = request.args.get("period")
    starting_date = parse(request.args.get("starting_date"))
    is_default_view = request.args.get("default_view") == "true"

    if period == "week":
        ending_date = relativedelta(days=7) + starting_date
    elif period == "month":
        ending_date = relativedelta(months=1) + starting_date
    elif period == "year":
        ending_date = relativedelta(years=1) + starting_date

    # add up all log length values in the time period
    logs = Log.query.filter(Log.date >= starting_date, Log.date < ending_date).all()

    if is_default_view:
        time_breakdown = [
            {"value": 0, "name": "Reading"},
            {"value": 0, "name": "Writing"},
            {"value": 0, "name": "Listening"},
            {"value": 0, "name": "Speaking"},
            {"value": 0, "name": "Flashcards"},
            {"value": 0, "name": "Other"},
        ]

        for log in logs:
            if log.type == "Reading":
                time_breakdown[0]["value"] += log.length / 60
            elif log.type == "Writing":
                time_breakdown[1]["value"] += log.length / 60
            elif log.type == "Listening":
                time_breakdown[2]["value"] += log.length / 60
            elif log.type == "Speaking":
                time_breakdown[3]["value"] += log.length / 60
            elif log.type == "Flashcards":
                time_breakdown[4]["value"] += log.length / 60
            else:
                time_breakdown[5]["value"] += log.length / 60
    else:
        time_breakdown = []
        # create unique time_breakdown list
        used_titles = set()
        for log in logs:
            if log.title not in used_titles:
                time_breakdown.append({"value": 0, "name": log.title})
                used_titles.add(log.title)

        for log in logs:
            # find index of the title in the time_breakdown list
            index = time_breakdown.index(
                [x for x in time_breakdown if x["name"] == log.title][0]
            )
            time_breakdown[index]["value"] += log.length / 60

    for element in time_breakdown:
        element["value"] = round(element["value"], 2)

    response = jsonify(time_breakdown=time_breakdown)
    # response.headers.add("Access-Control-Allow-Origin", "*")

    return response


# PLECO OR STATS UPDATE FILE
def parse_and_use_file(file):
    """
    Add in information in a file format.
    ---
    Custom Stats update file format:
    [name] [increment value]
    ...for example: [books_read] [1]
    ...or equally [chapters_read] [20]

    Books read and shows watched are updated randomly whenever finished reading or watching a show.
    Chapters read and characters read are updated weekly, with a notification sent to the user.

    This file can have any name.

    Supports:
    - characters_read
    - chapters_read
    - episodes_watched
    - books_read
    ---
    Vocab size is incremented through a Pleco export file. Just export *all* the flashcards in a long file,
    remove duplicates, and count the number of lines. This file will be called `pleco.txt`.
    ---
    Supports importing file named 'track - track.csv' from Google Sheets that looks like the following:

    ```csv
    	            02/19/22	02/20/22	02/21/22	02/22/22	02/23/22	02/24/22	02/25/22
        Chat	    0	        0	        0	        0	        0	        0	        0
        Class	    0	        0	        0	        0	        0	        0	        0
        Podcast	    0	        0	        0	        0	        0	        0	        0
        Shadowing	0	        0	        0	        0	        0	        0	        0
        Anki	    0	        0	        0	        0	        0	        0	        0
        TV	        0	        0	        0	        0	        0	        0	        0
        Pleco	    0	        0	        0	        0	        0	        0	        0
        Webnovel	0	        0	        0	        0	        0	        0	        0
    ```
    Where the zeros are the actual minutes for that time.
    """
    # parse the file (file.read())
    # use the data to create a new log
    # NOTE: custom file upload is for VOCAB TRACKING ONLY
    # to track time, upload screen time to the custom log

    user = User.query.filter_by(id=1).first()  # NOTE: hardcode...
    action_mapping = {
        "Chat": "Speaking",
        "Class": "Other",
        "Podcast": "Listening",
        "Audiobook": "Listening",
        "Shadowing": "Speaking",
        "Anki": "Flashcards",
        "Pleco": "Flashcards",
        "Webnovel": "Reading",
        "TV": "Listening",
    }

    # check if file is called pleco.txt
    if file.filename == "pleco.txt":
        # TODO: update character_size and vocab_size to read from latest statistic in database
        # get the number of lines in the file
        lines = file.readlines()
        # remove duplicate lines
        lines = list(set(lines))
        user.vocab_size = len(lines)
        db.session.commit()

        # calculate total character size
        joined = "".join([line.decode() for line in lines])
        only_chinese = re.findall(r"[\u4e00-\u9fff]+", joined)
        only_chinese = "".join(only_chinese)
        user.character_size = len(set(only_chinese))
        db.session.commit()

        # create the snapshots of this data
        snapshot = StatisticSnapshot("Vocab Size (Words)", user.vocab_size)
        db.session.add(snapshot)
        db.session.commit()
        snapshot = StatisticSnapshot("Vocab Size (Characters)", user.character_size)
        db.session.add(snapshot)

    elif file.filename == "stats.txt":
        # parse the file
        lines = file.readlines()

        # remove the newline character
        lines = [line.rstrip() for line in lines]

        # divide up each line into a list of the form [name, value]
        lines = [line.decode().split("\t") for line in lines]

        for line in lines:
            if line[0] == "books_read":
                user.books_read += int(line[1])
                db.session.commit()
                snapshot = StatisticSnapshot("Books Read", user.books_read)
                db.session.add(snapshot)
            elif line[0] == "chapters_read":
                user.chapters_read += int(line[1])
                db.session.commit()
                snapshot = StatisticSnapshot("Chapters Read", user.chapters_read)
                db.session.add(snapshot)
            elif line[0] == "episodes_watched":
                user.shows_watched += int(line[1])
                db.session.commit()
                snapshot = StatisticSnapshot(
                    "Episodes/Movies Watched", user.shows_watched
                )
                db.session.add(snapshot)
            elif line[0] == "characters_read":
                user.characters_read += int(line[1])
                db.session.commit()
                snapshot = StatisticSnapshot("Characters Read", user.characters_read)
                db.session.add(snapshot)

    elif file.filename == "track - track.csv":
        # parse the file
        lines = file.readlines()

        # remove the newline character
        lines = [line.rstrip() for line in lines]

        # divide up each line into a list of the form [name, value]
        lines = [line.decode().split(",") for line in lines]

        logs_to_add = []

        for line in lines[1:]:
            for i in range(1, len(line[1:]) + 1):
                if line[i] != "0":
                    log = Log(
                        title=line[0],
                        user_id=1,  # NOTE: hardcoded for prototype
                        length=int(line[i]),
                        type=action_mapping[line[0]],
                        language="zh",  # NOTE: hardcoded for prototype
                    )
                    log.date = parse(lines[0][i])  # follows mm-dd-yy format
                    logs_to_add.append(log)

        # add the logs to the database
        for addable_log in logs_to_add:
            db.session.add(addable_log)
        db.session.commit()

    db.session.commit()


    # Update my Notion stats page
    # https://heavenlypath.notion.site/Mythaar-ecebac2093c74f69914740949921d4f1
    # main website heavenlypath.notion.site is a curated collection of intermediate+ learner resources

    # NOTE: commented out given that stats are no longer being updated

    """
    STATS_LOG = "2795ae914ae7433e99831b40885175e7"
    NOTION_API_KEY = os.environ["NOTION_API_KEY"]

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_API_KEY}",
    }

    ############
    # fetch and clear all rows from database
    response = requests.request(
        "POST",
        "https://api.notion.com/v1/databases/" + STATS_LOG + "/query",
        headers=headers,
    )

    # get results dictionary from response
    results = response.json()["results"]

    # get the id of every row in results
    row_ids = [row["id"] for row in results]

    def delete_row(row_id, headers):
        url = f"https://api.notion.com/v1/pages/{row_id}"
        payload = {"archived": True}

        response = requests.request("PATCH", url, headers=headers, json=payload)
        return response

    for row_id in row_ids:
        delete_row(row_id, headers)

    ############
    # used to add something new to the database
    def add_new_row(headers, payload):
        url = f"https://api.notion.com/v1/pages"

        response = requests.request("POST", url, headers=headers, json=payload)
        return response

    total_hours = sum(
        [log.length / 60 for log in Log.query.filter_by(user_id=user.id).all()]
    )

    all_payloads = [
        {
            "parent": {
                "database_id": STATS_LOG,
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": "Characters Read",
                            }
                        }
                    ]
                },
                "Value": {"number": user.characters_read},
            },
        },
        {
            "parent": {
                "database_id": STATS_LOG,
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": "Chapters Read",
                            }
                        }
                    ]
                },
                "Value": {"number": user.chapters_read},
            },
        },
        {
            "parent": {
                "database_id": STATS_LOG,
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": "TV Episodes/Movies Watched",
                            }
                        }
                    ]
                },
                "Value": {"number": user.shows_watched},
            },
        },
        {
            "parent": {
                "database_id": STATS_LOG,
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": "Books Read",
                            }
                        }
                    ]
                },
                "Value": {"number": user.books_read},
            },
        },
        {
            "parent": {
                "database_id": STATS_LOG,
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": "Study Hours (2022 onwards)",
                            }
                        }
                    ]
                },
                "Value": {"number": round(total_hours, 2)},
            },
        },
    ]

    all_payloads = reversed(all_payloads)

    for payload in all_payloads:
        add_new_row(headers, payload)
    """

    return jsonify(success=True)
