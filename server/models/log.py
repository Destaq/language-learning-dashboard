from extensions import db


class Log(db.Model):
    """
    Any log used to track progress. This can be a custom log, which is written down, or a log that is built by analyzing some of the user inputted data (e.g. from Pleco or Anki).
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    length = db.Column(db.Integer, nullable=True)  # time in minutes
    type = db.Column(db.String(80), nullable=True)  # 'writing', 'reading', 'speaking', 'listening'...
    
    # iso 639-1 language code
    language = db.Column(db.String(2), nullable=True)

    def __init__(self, text, title, user_id, length, type, language):
        self.text = text
        self.title = title
        self.user_id = user_id
        self.length = length
        self.type = type
        self.language = language
