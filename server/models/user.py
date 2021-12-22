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

    def __init__(self, username):
        self.username = username

    def get_active_goals(self):
        resp = {}
        for goal in self.goals:
            if (goal.deadline < datetime.now()) or (goal.deadline > datetime.now() and goal.completed == False):
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
                "title": "Watched Show",
                "text": "Watched Chinese television content.",
                "length": 15,
                "type": "listening",
                "language": "zh",
                "user_id": self.id
            },
            "chinese_class": {
                "title": "Chinese Class",
                "text": "Had a Chinese class with my tutor.",
                "length": 60,
                "type": "listening",
                "language": "zh",
                "user_id": self.id
            },
            "podcast": {
                "title": "Podcast",
                "text": "Listened to a podcast in Chinese.",
                "length": 30,
                "type": "listening",
                "language": "zh",
                "user_id": self.id
            },
            "shadowing": {
                "title": "Shadowing",
                "text": "Shadowed some Chinese content.",
                "length": 10,
                "type": "speaking",
                "language": "zh",
                "user_id": self.id
            },
            "workbook": {
                "title": "Workbook",
                "text": "Did some workbook exercises.",
                "length": 45,
                "type": "other",
                "language": "zh",
                "user_id": self.id
            }
        }
