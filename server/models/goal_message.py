from extensions import db


class GoalMessage(db.Model):
    """
    A GoalMessage can be thought of as a special type of note. It is a message that is used to motivate the user to do something. These are set by the user themselves, and have two types: targets and reflections.

    At any point in time, users can create a todo-list of goals, and then set a target for each goal. They will also have a deadline for completing the goal. When the deadline is reached, they will be prompted for a reflection.

    There will be syntax highlighting, checklisting, and other features etc. based on NLP of the target.
    """

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)  # 'target', 'reflection'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.Text)
    set_time = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    deadline = db.Column(db.DateTime, nullable=True)  # null if a reflection

    def __init__(self, type, user_id, text, set_time, deadline=None):
        self.type = type
        self.user_id = user_id
        self.text = text
        self.set_time = set_time
        self.deadline = deadline
