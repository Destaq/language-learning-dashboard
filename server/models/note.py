from extensions import db


class Note(db.Model):
    """
    A note is any message that can be attached to a time period. I envision this being later searchable in a calendar view, and including stuff like main resources, motivational quotes, comments on how the day went, etc.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.Text)

    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id
