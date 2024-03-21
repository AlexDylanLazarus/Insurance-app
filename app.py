from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


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

if __name__ == "__main__":
    app.run(debug=True)


@app.get("/cards")
def get_cards():
    return jsonify(cards)


@app.post("/cards")
def post_cards():
    new_card = request.json
    card_id = [int(card["id"]) for card in cards]
    max_id = max(card_id) if card_id else 0
    new_card["id"] = str(max_id + 1)
    cards.append(new_card)
    result = {"message": "Card Added Successfully"}
    return jsonify(result), 201


@app.get("/cards/<id>")
def get_card_by_id(id):
    filtered_card = next((card for card in cards if card["id"] == id), None)
    if filtered_card:
        return jsonify(filtered_card)
    else:
        return jsonify({"message": "Card not found"}), 404


@app.delete("/cards/<id>")
def delete_card(id):
    id_for_deletion = next((card for card in cards if card["id"] == id), None)
    if id_for_deletion:
        print(cards.remove(id_for_deletion))
        return jsonify({"message": "deleted successfully", "data": id_for_deletion})
    else:
        return jsonify({"message": "Card not found"}), 404


@app.put("/cards/<id>")
def update_cards(id):
    update_card = request.json
    id_for_updating = next((card for card in cards if card["id"] == id), None)
    if id_for_updating:
        id_for_updating.update(update_card)
        return jsonify(
            {"message": "Card updated successfully", "data": id_for_updating}
        )
    else:
        return jsonify({"message": "Card not found"}), 404


@app.post("/users")
def post_cards():
    new_user = request.json
    user_id = [int(user["id"]) for user in users]
    max_id = max(user_id) if user_id else 0
    new_user["id"] = str(max_id + 1)
    cards.append(new_user)
    result = {"message": "User Added Successfully"}
    return jsonify(result), 201


@app.get("/users/<id>")
def get_user_by_id(id):
    filtered_user = next((user for user in users if user["id"] == id), None)
    if filtered_user:
        return jsonify(filtered_user)
    else:
        return jsonify({"message": "User not found"}), 404


@app.delete("/users/<id>")
def delete_user(id):
    id_for_deletion = next((user for user in users if users["id"] == id), None)
    if id_for_deletion:
        print(users.remove(id_for_deletion))
        return jsonify({"message": "deleted successfully", "data": id_for_deletion})
    else:
        return jsonify({"message": "User not found"}), 404


@app.put("/users/<id>")
def update_users(id):
    update_user = request.json
    id_for_updating = next((user for user in users if user["id"] == id), None)
    if id_for_updating:
        id_for_updating.update(update_user)
        return jsonify(
            {"message": "User updated successfully", "data": id_for_updating}
        )
    else:
        return jsonify({"message": "User not found"}), 404
