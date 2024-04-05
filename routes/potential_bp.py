from flask import Blueprint, render_template, jsonify, request
from models.potential_customers import PotentialCustomers
from extensions import db

potential_bp = Blueprint("potential_bp", __name__)


@potential_bp.route("/potential_customers", methods=["GET"])
def get_potential_customers():
    customers = PotentialCustomers.query.all()
    return jsonify([customer.to_dict() for customer in customers])


@potential_bp.route("/potential_customers/<string:customer_id>", methods=["GET"])
def get_potential_customer(customer_id):
    customer = PotentialCustomers.query.get(customer_id)
    if customer:
        return jsonify(customer.to_dict())
    else:
        return jsonify({"message": "Potential customer not found"}), 404


@potential_bp.route("/potential_customers", methods=["POST"])
def add_potential_customer():
    new_customer_data = request.json
    new_customer = PotentialCustomers(**new_customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Potential customer added successfully"}), 201


@potential_bp.route("/potential_customers/<string:customer_id>", methods=["PUT"])
def update_potential_customer(customer_id):
    customer = PotentialCustomers.query.get(customer_id)
    if customer:
        customer_data = request.json
        for key, value in customer_data.items():
            setattr(customer, key, value)
        db.session.commit()
        return jsonify({"message": "Potential customer updated successfully"}), 200
    else:
        return jsonify({"message": "Potential customer not found"}), 404


@potential_bp.route("/potential_customers/<string:customer_id>", methods=["DELETE"])
def delete_potential_customer(customer_id):
    customer = PotentialCustomers.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Potential customer deleted successfully"}), 200
    else:
        return jsonify({"message": "Potential customer not found"}), 404
