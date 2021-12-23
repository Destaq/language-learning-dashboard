from flask import Blueprint, request, jsonify
from extensions import db
from models.chengyu import Chengyu

chengyu_bp = Blueprint("chengyu", __name__)


def serialize(chengyu_object):
    return {
        "derivation": chengyu_object.derivation,
        "example": chengyu_object.example,
        "explanation": chengyu_object.explanation,
        "pinyin": chengyu_object.pinyin,
        "word": chengyu_object.word,
        "abbreviation": chengyu_object.abbreviation,
    }


@chengyu_bp.route("/random-chengyu", methods=["GET"])
def random_chengyu():
    # pick a random chengyu from the database
    chengyu = "1234567"
    itslength = len(chengyu)
    while itslength > 6:
        chengyu = Chengyu.query.order_by(db.func.random()).first()
        itslength = len(chengyu.word)
    return jsonify({"chengyu": serialize(chengyu)})
