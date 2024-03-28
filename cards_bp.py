from flask import Blueprint, render_template, jsonify, request
from app import cards


cards_bp = Blueprint("cards_bp", __name__)


@cards_bp.route("/", methods=["GET"])
def get_all_cards():
    return jsonify(cards)


@cards_bp.route("/<id>", methods=["GET"])
def get_card_by_id(id):
    filtered_card = next((card for card in cards if card["id"] == id), None)
    if filtered_card:
        return jsonify(filtered_card)
    else:
        return jsonify({"message": "Card not found"}), 404


@cards_bp.route("/", methods=["POST"])
def add_card():
    new_card = request.json
    card_id = [int(card["id"]) for card in cards]
    max_id = max(card_id) if card_id else 0
    new_card["id"] = str(max_id + 1)
    cards.append(new_card)
    result = {"message": "Card Added Successfully"}
    return jsonify(result), 201


@cards_bp.route("/<id>", methods=["PUT"])
def update_card(id):
    update_card = request.json
    card_to_update = next((card for card in cards if card["id"] == id), None)
    if card_to_update:
        card_to_update.update(update_card)
        return jsonify({"message": "Card updated successfully", "data": card_to_update})
    else:
        return jsonify({"message": "Card not found"}), 404


@cards_bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    id_for_deletion = next((card for card in cards if card["id"] == id), None)
    if id_for_deletion:
        cards.remove(id_for_deletion)
        return jsonify({"message": "deleted successfully", "data": id_for_deletion})
    else:
        return jsonify({"message": "Card not found"}), 404
