from flask import Flask, jsonify, request, render_template, redirect, url_for
import random

app = Flask(__name__)

insurance_policies = [
    {
        "policy_id": 1,
        "policy_name": "Car Insurance",
        "coverage": ["Accident", "Theft", "Liability"],
        "premium": 500,
        "deductible": 100,
        "details": "Car insurance is a financial product that provides protection against losses incurred due to accidents, theft, or damage to vehicles. When purchasing car insurance, individuals select a policy and pay a premium to an insurance company in exchange for coverage. Policies offer various levels of coverage, including liability, collision, comprehensive, and uninsured/underinsured motorist coverage. In the event of a covered incident, policyholders file a claim, and the insurer assesses and approves it, providing financial compensation up to the policy limits. Policyholders may have to pay a deductible before receiving compensation. Car insurance policies typically last for a set period, and at renewal, policyholders can adjust coverage or switch insurers. Understanding policy terms and conditions is crucial to ensure adequate coverage when needed, as car insurance is often mandatory for driving legally on public roads, with specific requirements varying by location and circumstances.",
        "image": "http://surl.li/ryexr",
    },
    {
        "policy_id": 2,
        "policy_name": "Home Insurance",
        "coverage": ["Fire", "Flood", "Theft"],
        "premium": 800,
        "deductible": 200,
        "details": "Home insurance is a financial product that safeguards homeowners against financial losses resulting from damages to their properties, including the physical structure and personal belongings, as well as liability for accidents that occur on the property. Homeowners purchase policies and pay premiums to insurance companies, selecting coverage options such as dwelling coverage, personal property coverage, liability protection, and additional living expenses coverage. When an insured event, such as fire, theft, or natural disaster, occurs, homeowners file a claim with their insurance company, which assesses the claim and provides financial compensation up to the policy limits. Like car insurance, homeowners may need to pay a deductible before receiving compensation. Home insurance policies typically renew annually, allowing homeowners to adjust coverage as needed. Understanding policy terms and conditions is essential for ensuring adequate coverage, as home insurance is often required by mortgage lenders and varies in requirements and options based on location and individual circumstances.",
        "image": "http://surl.li/ryeyo",
    },
    {
        "policy_id": 3,
        "policy_name": "Health Insurance",
        "coverage": ["Hospitalization", "Prescription Drugs", "Surgery"],
        "premium": 1000,
        "deductible": 300,
        "details": "Health insurance is a financial product designed to mitigate the cost of medical expenses for individuals and families. Policyholders pay premiums to health insurance companies in exchange for coverage that helps pay for healthcare services such as doctor visits, hospital stays, prescription medications, and preventive care. Health insurance policies typically offer various types of coverage, including hospitalization, outpatient care, emergency services, prescription drugs, and mental health services, among others. When policyholders need medical care, they may be required to pay a copayment, coinsurance, and/or meet a deductible before the insurance kicks in. Health insurance plans may also have networks of healthcare providers, and using in-network providers can result in lower out-of-pocket costs for policyholders. Understanding policy terms, coverage limits, and network restrictions is crucial for making informed healthcare decisions. Health insurance is often obtained through employers, government programs, or purchased independently, and regulations and coverage options vary by location and individual circumstances.",
        "image": "https://www.sanlam.co.za/personal/insurance/healthsolutions/PublishingImages/health-solutions-banner-desktop.png",
    },
]

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
        "Street_Address": "2 Tree Street",
        "Zip_code": "1999",
        "Suburb": "Beverley Hills",
        "City": "Cape Town",
        "Country": "South Africa",
        "sex": "Male",
        "policies": insurance_policies[1],
    }
]


total_cards = 20
cards = [{"id": str(i), "name": "Try again", "win": False} for i in range(total_cards)]
uber_voucher_index = random.randint(0, total_cards - 1)
cards[uber_voucher_index]["win"] = True


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user exists and the password is correct
        user = next(
            (u for u in users if u["Email"] == email and u["Password"] == password),
            None,
        )
        if user:
            if user["Credits"] > 1:
                # Deduct credits
                user["Credits"] -= 2
                random.shuffle(cards)
                return render_template("index.html", user=user, cards=cards)
            else:
                return "Insufficient credits. Please add more credits to play."
        else:
            # If user is not found or password is incorrect, render login page with error message
            return render_template(
                "login.html", error="User not found or incorrect password."
            )
    else:
        # Render the login page without requiring form data
        return render_template("login.html")


@app.route("/pol")
def pol():
    return render_template("pol.html", policies=insurance_policies)


@app.route("/get_a_quote")
def quote():
    return render_template("get_a_quote.html", policies=insurance_policies)


@app.route("/profile")
def profile():
    return render_template("profile.html", users=users[0])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print("Email:", email)
        print("Password:", password)

        # Print out the users list for debugging
        print("Users:", users)
        user = next(
            (u for u in users if u["Email"] == email and u["Password"] == password),
            None,
        )
        if user:
            return render_template("index.html", user=user, cards=cards)
        else:
            return "User not found"
    else:
        return render_template("login.html")


@app.route("/try_again", methods=["POST"])
def try_again():
    user_id = request.form.get("user_id")
    # Retrieve user data based on user_id
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        if user["Credits"] > 1:
            # Deduct credits
            user["Credits"] -= 2
            # Shuffle the cards
            random.shuffle(cards)
            return render_template("index.html", user=user, cards=cards)
        else:
            return "Insufficient credits. Please add more credits to play."
    else:
        return "User not found"  # Handle case where user is not found


@app.route("/after_login", methods=["POST"])
def after_login():
    email = request.form.get("email")
    password = request.form.get("password")
    go_ahead = next(
        (
            user
            for user in users
            if user["Password"] == password and user["Email"] == email
        ),
        None,
    )
    if go_ahead:
        return render_template("index.html", user=go_ahead)
    else:
        return "Invalid email or password"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Retrieve form data
        first_name = request.form.get("Name")
        last_name = request.form.get("Last_name")
        date_of_birth = request.form.get("Date_of_birth")
        email = request.form.get("email")
        password = request.form.get("Password")
        phone_number = request.form.get("Phone_number")
        street_address = request.form.get("Street_Address")
        zip_code = request.form.get("Zip_code")
        suburb = request.form.get("Suburb")
        city = request.form.get("City")
        country = request.form.get("Country")
        gender = request.form.get("gender")
        new_user = {
            "Name": first_name,
            "Last_name": last_name,
            "Date_of_birth": date_of_birth,
            "Email": email,
            "Password": password,
            "Phone_number": phone_number,
            "Credits": 10,
            "Street_Address": street_address,
            "Zip_code": zip_code,
            "Suburb": suburb,
            "City": city,
            "Country": country,
            "sex": gender,
        }

        # Add the new user to the list of users
        users.append(new_user)

        # Redirect to login page after successful registration
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


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


@app.route("/policies", methods=["GET"])
def get_policies():
    return jsonify(insurance_policies)


@app.route("/policies/<int:policy_id>", methods=["GET"])
def get_policy(policy_id):
    policy = next(
        (policy for policy in insurance_policies if policy["policy_id"] == policy_id),
        None,
    )
    if policy:
        return jsonify(policy)
    else:
        return jsonify({"message": "Policy not found"}), 404


@app.get("/pol/<int:policy_id>")
def get_policy_page(policy_id):
    policy = next(
        (policy for policy in insurance_policies if policy["policy_id"] == policy_id),
        None,
    )
    if policy:
        return render_template("policy_details.html", policy=policy)
    else:
        return jsonify({"message": "Policy not found"}), 404


@app.route("/policies", methods=["POST"])
def add_policy():
    new_policy = request.json
    insurance_policies.append(new_policy)
    return jsonify({"message": "Policy added successfully"}), 201


@app.route("/policies/<int:policy_id>", methods=["PUT"])
def update_policy(policy_id):
    policy_to_update = next(
        (policy for policy in insurance_policies if policy["policy_id"] == policy_id),
        None,
    )
    if policy_to_update:
        policy_to_update.update(request.json)
        return jsonify({"message": "Policy updated successfully"}), 200
    else:
        return jsonify({"message": "Policy not found"}), 404


@app.route("/policies/<int:policy_id>", methods=["DELETE"])
def delete_policy(policy_id):
    global insurance_policies
    initial_length = len(insurance_policies)
    insurance_policies = [
        policy for policy in insurance_policies if policy["policy_id"] != policy_id
    ]
    if len(insurance_policies) < initial_length:
        return jsonify({"message": "Policy deleted successfully"}), 200
    else:
        return jsonify({"message": "Policy not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
