from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    # profile_pic coming soon
    goals = db.relationship("GoalMessage", backref="user", lazy=True)
    milestones = db.relationship("Milestone", backref="user", lazy=True)
    notes = db.relationship("Note", backref="user", lazy=True)
    logs = db.relationship("Log", backref="user", lazy=True)
    actions = db.relationship("Action", backref="user", lazy=True)
    vocab_size = db.Column(db.Integer, nullable=False, default=0)

    characters_read = db.Column(db.Integer, nullable=False, default=0)
    chapters_read = db.Column(db.Integer, nullable=False, default=0)
    books_read = db.Column(db.Integer, nullable=False, default=0)
    shows_watched = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, username):
        self.username = username

    def get_active_goals(self):
        resp = {}
        for goal in self.goals:
            if (goal.deadline < datetime.now() and goal.completed == False) or (goal.deadline > datetime.now()):
                resp[goal.id] = {
                    "description": goal.description,
                    "set_time": goal.set_time,
                    "completed": goal.completed,
                    "deadline": goal.deadline,
                    "id": goal.id
                }
        return resp

    def get_milestones(self):
        resp = {}
        for milestone in self.milestones:
            resp[milestone.id] = {
                "description": milestone.description,
                "set_time": milestone.set_time,
                "completed": milestone.completed,
            }
        return resp

    def get_notes(self):
        resp = {}
        for note in self.notes:
            resp[note.id] = {
                "description": note.description,
                "set_time": note.set_time,
                "completed": note.completed,
            }

    def get_actions(self):
        # return a dictionary of possible quick log actions
        # TODO: this would be an individual database for every user
        # TODO: set in-app Sunday evening reminder to input data (readibu, anki, pleco, hellotalk)
        # NOTE: can also input manually and then subtract from file
        return {
            "show": {
                "title": "TV",
                "length": 15,
                "type": "listening",
                "language": "zh",
                "user_id": self.id
            },
            "chinese_class": {
                "title": "Class",
                "length": 60,
                "type": "listening",
                "language": "zh",
                "user_id": self.id
            },
            "podcast": {
                "title": "Podcast",
                "length": 30,
                "type": "listening",
                "language": "zh",
                "user_id": self.id
            },
            "shadowing": {
                "title": "Shadowing",
                "length": 10,
                "type": "speaking",
                "language": "zh",
                "user_id": self.id
            },
            "workbook": {
                "title": "Workbook",
                "length": 45,
                "type": "other",
                "language": "zh",
                "user_id": self.id
            }
        }
