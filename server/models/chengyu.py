from extensions import db


class Chengyu(db.Model):
    """
    Database chengyu entry, which is randomly selected to be displayed.
    """

    id = db.Column(db.Integer, primary_key=True)

    derivation = db.Column(db.String)
    example = db.Column(db.String)
    explanation = db.Column(db.String)
    pinyin = db.Column(db.String)
    word = db.Column(db.String, unique=True)
    abbreviation = db.Column(db.String)

    def __init__(self, derivation, example, explanation, pinyin, word, abbreviation):
        self.derivation = derivation
        self.example = example
        self.explanation = explanation
        self.pinyin = pinyin
        self.word = word
        self.abbreviation = abbreviation
