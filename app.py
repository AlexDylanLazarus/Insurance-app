from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

total_cards = 20
cards = [{"id": str(i), "name": "Try again", "win": False} for i in range(total_cards)]
uber_voucher_index = random.randint(0, total_cards - 1)
cards[uber_voucher_index]["win"] = True


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        user = next((u for u in users if u["id"] == user_id), None)
        if user:
            user["Credits"] -= 2
            random.shuffle(cards)
            return render_template("index.html", user=user, cards=cards)
        else:
            return "User not found"
    else:
        return render_template("index.html", user=users[0], cards=cards)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


users = [
    {
        "id": "1",
        "Name": "Alex",
        "Last_name": "Lazarus",
        "Date_of_birth": "4 Jul 2002",
        "Password": "Alex1234!",
        "Email": "alexdylanlazarus@gmail.com",
        "Phone_number": "0633603171",
        "Credits": 100,
        "Street Address": "2 Tree Street",
        "Zip code": "1999",
        "Suburb": "Beverley Hills",
        "City": "Cape Town",
        "Country": "South Africa",
    }
]

cards = [
    {"id": "100", "name": "Try again", "win": False},
    {"id": "101", "name": "Uber Voucher", "win": True},
]


@app.route("/cards")
def get_cards():
    return jsonify(cards)


@app.route("/cards", methods=["POST"])
def post_card():
    new_card = request.json
    card_id = [int(card["id"]) for card in cards]
    max_id = max(card_id) if card_id else 0
    new_card["id"] = str(max_id + 1)
    cards.append(new_card)
    result = {"message": "Card Added Successfully"}
    return jsonify(result), 201


@app.route("/cards/<id>")
def get_card_by_id(id):
    filtered_card = next((card for card in cards if card["id"] == id), None)
    if filtered_card:
        return jsonify(filtered_card)
    else:
        return jsonify({"message": "Card not found"}), 404


@app.route("/cards/<id>", methods=["DELETE"])
def delete_card(id):
    id_for_deletion = next((card for card in cards if card["id"] == id), None)
    if id_for_deletion:
        cards.remove(id_for_deletion)
        return jsonify({"message": "deleted successfully", "data": id_for_deletion})
    else:
        return jsonify({"message": "Card not found"}), 404


@app.route("/cards/<id>", methods=["PUT"])
def update_card(id):
    update_card = request.json
    card_to_update = next((card for card in cards if card["id"] == id), None)
    if card_to_update:
        card_to_update.update(update_card)
        return jsonify({"message": "Card updated successfully", "data": card_to_update})
    else:
        return jsonify({"message": "Card not found"}), 404


@app.route("/users", methods=["POST"])
def post_user():
    new_user = request.json
    user_id = [int(user["id"]) for user in users]
    max_id = max(user_id) if user_id else 0
    new_user["id"] = str(max_id + 1)
    users.append(new_user)
    result = {"message": "User Added Successfully"}
    return jsonify(result), 201


@app.route("/users/<id>")
def get_user_by_id(id):
    filtered_user = next((user for user in users if user["id"] == id), None)
    if filtered_user:
        return jsonify(filtered_user)
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user_to_delete = next((user for user in users if user["id"] == id), None)
    if user_to_delete:
        users.remove(user_to_delete)
        return jsonify({"message": "deleted successfully", "data": user_to_delete})
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    update_user = request.json
    user_to_update = next((user for user in users if user["id"] == id), None)
    if user_to_update:
        user_to_update.update(update_user)
        return jsonify({"message": "User updated successfully", "data": user_to_update})
    else:
        return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
