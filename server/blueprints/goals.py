from flask import Blueprint, request, jsonify
from extensions import db
from models.goal_message import GoalMessage
from models.user import User

goal_bp = Blueprint("goal", __name__)


@goal_bp.route("/weekly-goals", methods=["GET"])
def display_user_goals():
    user = User.query.filter_by(id=1).first()
    return jsonify(goals=user.get_goals())


@goal_bp.route("/submit-new-goal", methods=["POST"])
def submit_new_goal():
    user = User.query.filter_by(id=1).first()  # NOTE: hardcoded

    goal_message = GoalMessage(
        user_id=user.id,
        description=request.json["description"],
        completed=False,
        deadline=request.json["deadline"],
    )
    db.session.add(goal_message)
    db.session.commit()
    return jsonify(success=True)


@goal_bp.route("/edit-goal", methods=["POST"])
def edit_goal():
    goal_message = GoalMessage.query.filter_by(id=request.json["id"]).first()
    goal_message.description = request.json["description"]
    goal_message.deadline = request.json["deadline"]
    goal_message.completed = request.json["completed"]
    db.session.commit()
    return jsonify(success=True)


@goal_bp.route("/delete-goal", methods=["POST"])
def delete_goal():
    goal_message = GoalMessage.query.filter_by(id=request.json["id"]).first()
    db.session.delete(goal_message)
    db.session.commit()
    return jsonify(success=True)
