from extensions import db

class Milestone(db.Model):
    """
    A database of quantifiable milestones (which can also be custom set). These will be displayed to the user when they reach the milestone, and be used as a form of motivation.
    """

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=True)
    text = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(80), nullable=True) # 'writing', 'reading', 'speaking', 'listening'...

    def __init__(self, value, text, type):
        self.value = value
        self.text = text
        self.type = type
