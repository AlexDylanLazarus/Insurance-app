from flask import Blueprint, render_template, jsonify, request
from models.userinsurance import UserInsurance
from extensions import db

userinsurance_bp = Blueprint("userinsurance_bp", __name__)


# Create
@userinsurance_bp.route("/userinsurance", methods=["POST"])
def create_user_insurance():
    data = request.json
    new_user_insurance = UserInsurance(**data)
    db.session.add(new_user_insurance)
    db.session.commit()
    return jsonify(new_user_insurance.to_dict()), 201


# Read
@userinsurance_bp.route("/userinsurance/<user_id>/<policy_id>", methods=["GET"])
def get_user_insurance(user_id, policy_id):
    user_insurance = UserInsurance.query.filter_by(
        user_id=user_id, policy_id=policy_id
    ).first()
    if user_insurance:
        return jsonify(user_insurance.to_dict()), 200
    else:
        return jsonify({"error": "User insurance not found"}), 404


# Update
@userinsurance_bp.route("/userinsurance/<user_id>/<policy_id>", methods=["PUT"])
def update_user_insurance(user_id, policy_id):
    user_insurance = UserInsurance.query.filter_by(
        user_id=user_id, policy_id=policy_id
    ).first()
    if user_insurance:
        data = request.json
        user_insurance.update(data)
        db.session.commit()
        return jsonify(user_insurance.to_dict()), 200
    else:
        return jsonify({"error": "User insurance not found"}), 404


# Delete
@userinsurance_bp.route("/userinsurance/<user_id>/<policy_id>", methods=["DELETE"])
def delete_user_insurance(user_id, policy_id):
    user_insurance = UserInsurance.query.filter_by(
        user_id=user_id, policy_id=policy_id
    ).first()
    if user_insurance:
        db.session.delete(user_insurance)
        db.session.commit()
        return jsonify({"message": "User insurance deleted successfully"}), 200
    else:
        return jsonify({"error": "User insurance not found"}), 404


# List all user insurances
@userinsurance_bp.route("/userinsurances", methods=["GET"])
def list_user_insurances():
    user_insurances = UserInsurance.query.all()
    return (
        jsonify([user_insurance.to_dict() for user_insurance in user_insurances]),
        200,
    )
