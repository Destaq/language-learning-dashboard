from extensions import db

class Action(db.Model):
    """
    A repeatable action that is shown daily.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, title, description):
        self.user_id = user_id
        self.title = title
        self.description = description
