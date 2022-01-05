from extensions import db


class StatisticSnapshot(db.Model):
    """
    User statistics are tracked over time. This is a snapshot of some statistic at some time.

    In my case, used to track:
    - vocab size (words)
    - vocab size (characters)
    - characters read
    - chapters read
    - books read
    - episodes/movies watched

    These six are the core statistics that are tracked, others can be inferred from the log or goal models.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    name = db.Column(db.String(80), nullable=False)  # unique string name for each statistic
    value = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, name, value, user_id=1):
        self.name = name
        self.value = value
        self.user_id = user_id  # TODO: make public
