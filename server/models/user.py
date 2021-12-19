from extensions import db


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
