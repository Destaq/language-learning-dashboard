from extensions import db


class GoalMessage(db.Model):
    """
    A GoalMessage can be thought of as a special type of note. It is a message that is used to motivate the user to do something. These are set by the user themselves, and have two types: targets and reflections.

    At any point in time, users can create a todo-list of goals, and then set a target for each goal. They will also have a deadline for completing the goal. When the deadline is reached, they will be prompted for a reflection.

    There will be syntax highlighting, checklisting, and other features etc. based on NLP of the target.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.Text)
    set_time = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    completed = db.Column(db.Boolean, nullable=False, default=False)
    deadline = db.Column(db.DateTime, nullable=True)  # null if a reflection

    def __init__(self, user_id, description, completed=False, deadline=None):
        self.user_id = user_id
        self.description = description
        self.completed = completed
        self.deadline = deadline
