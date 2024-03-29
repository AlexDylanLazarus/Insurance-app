from flask import Blueprint, render_template, jsonify, request
from app import User, db

users_bp = Blueprint("users_bp", __name__)


@users_bp.route("/users", methods=["POST"])
def post_user():
    new_user_data = request.json
    new_user = User(**new_user_data)
    db.session.add(new_user)
    db.session.commit()
    result = {"message": "User Added Successfully"}
    return jsonify(result), 201


@users_bp.route("/users/<id>")
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({"message": "User not found"}), 404


@users_bp.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return (
            jsonify({"message": "User deleted successfully", "data": user.to_dict()}),
            200,
        )
    else:
        return jsonify({"message": "User not found"}), 404


@users_bp.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user_data = request.json
    user = User.query.get(id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.session.commit()
        return (
            jsonify({"message": "User updated successfully", "data": user.to_dict()}),
            200,
        )
    else:
        return jsonify({"message": "User not found"}), 404
