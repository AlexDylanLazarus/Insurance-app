from flask import Blueprint, render_template, jsonify, request
from app import Insurance, db

insurance_bp = Blueprint("insurance_bp", __name__)


@insurance_bp.route("/policies", methods=["GET"])
def get_policies():
    policies = Insurance.query.all()
    return jsonify([policy.to_dict() for policy in policies])


@insurance_bp.route("/policies/<int:policy_id>", methods=["GET"])
def get_policy(policy_id):
    policy = Insurance.query.get(policy_id)
    if policy:
        return jsonify(policy.to_dict())
    else:
        return jsonify({"message": "Policy not found"}), 404


@insurance_bp.route("/policies", methods=["POST"])
def add_policy():
    new_policy_data = request.json
    new_policy = Insurance(**new_policy_data)
    db.session.add(new_policy)
    db.session.commit()
    return jsonify({"message": "Policy added successfully"}), 201


@insurance_bp.route("/policies/<int:policy_id>", methods=["PUT"])
def update_policy(policy_id):
    policy = Insurance.query.get(policy_id)
    if policy:
        policy_data = request.json
        for key, value in policy_data.items():
            setattr(policy, key, value)
        db.session.commit()
        return jsonify({"message": "Policy updated successfully"}), 200
    else:
        return jsonify({"message": "Policy not found"}), 404


@insurance_bp.route("/policies/<int:policy_id>", methods=["DELETE"])
def delete_policy(policy_id):
    policy = Insurance.query.get(policy_id)
    if policy:
        db.session.delete(policy)
        db.session.commit()
        return jsonify({"message": "Policy deleted successfully"}), 200
    else:
        return jsonify({"message": "Policy not found"}), 404
