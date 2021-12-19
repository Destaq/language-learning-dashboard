from extensions import db

class Milestone(db.Model):
    """
    A database of quantifiable milestones (which can also be custom set). These will be displayed to the user when they reach the milestone, and be used as a form of motivation.
    """

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=True)
    text = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(80), nullable=True) # 'writing', 'reading', 'speaking', 'listening'...
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self, value, text, type, user_id=None):
        self.value = value
        self.text = text
        self.type = type
        self.user_id = user_id
