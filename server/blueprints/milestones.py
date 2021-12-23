# both automatic vocab and manual user milestones are implemented in this blueprint.
from flask import Blueprint, request, jsonify
from extensions import db
from models.milestone import Milestone
from models.user import User

milestone_bp = Blueprint("milestone", __name__)

milestones = [
    50,
    100,
    250,
    500,
    700,
    1000,
    1500,
    2000,
    3000,
    5000,
    7500,
    10000,
    15000,
    20000,
    25000,
    30000,
    35000,
    40000,
    45000,
    50000,
    60000,
    75000,
    100000,
]


@milestone_bp.route("/get-vocab-size-and-milestone", methods=["GET"])
def get_vocab_size_and_milestone():
    # return vocab size and the closest milestone that hasn't been reached
    user = User.query.filter_by(id=1).first()  # NOTE: hardcoded
    vocab_size = user.vocab_size
    for milestone in milestones:
        if vocab_size < milestone:
            return jsonify(
                vocab_size=vocab_size,
                milestone=milestone,
            )

