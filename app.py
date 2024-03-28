import os
from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
)
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import uuid


load_dotenv()

app = Flask(__name__)

connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # db.create_all()
except Exception as e:
    print("Error connecting to the database:", e)


total_cards = 20
cards = [{"id": str(i), "name": "Try again", "win": False} for i in range(total_cards)]
uber_voucher_index = random.randint(0, total_cards - 1)
cards[uber_voucher_index]["win"] = True


class Insurance(db.Model):
    __tablename__ = "insurance_policies"
    policy_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    policy_name = db.Column(db.String(255))
    coverage = db.Column(db.ARRAY(db.String()))
    premium = db.Column(db.Float)
    deductible = db.Column(db.Float)
    details = db.Column(db.String(1000))
    image_url = db.Column(db.String(255))

    # JSON
    def to_dict(self):
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "coverage": self.coverage,
            "deductible": self.deductible,
            "details": self.details,
            "image_url": self.image_url,
        }


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    Name = db.Column(db.String(255))
    Last_name = db.Column(db.String(255))
    Date_of_birth = db.Column(db.Date)
    Password = db.Column(db.String(255))
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Phone_number = db.Column(db.String(255))
    Credits = db.Column(db.Integer)
    Street_Address = db.Column(db.String(255))
    Zip_code = db.Column(db.String(255))
    Suburb = db.Column(db.String(255))
    City = db.Column(db.String(255))
    Country = db.Column(db.String(255))
    sex = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "Name": self.Name,
            "Last_name": self.Last_name,
            "Date_of_birth": self.Date_of_birth,
            "Password": self.Password,
            "Email": self.Email,
            "Phone_number": self.Phone_number,
            "Credits": self.Credits,
            "Street_Address": self.Street_Address,
            "Zip_code": self.Zip_code,
            "Surburb": self.Suburb,
            "City": self.City,
            "Country": self.Country,
            "sex": self.sex,
        }


from cards_bp import cards_bp


app.register_blueprint(cards_bp, url_prefix="/cards")


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Query the database to find a user with the provided email and password
        user = User.query.filter_by(Email=email, Password=password).first()

        if user:
            if user.Credits > 1:
                # Deduct credits
                user.Credits -= 2
                db.session.commit()  # Update the user's credits in the database
                random.shuffle(cards)
                # Redirect to the index.html page after successful login
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
    insurance_policies = Insurance.query.all()
    return render_template("pol.html", policies=insurance_policies)


@app.route("/get_a_quote")
def quote():
    insurance_policies = Insurance.query.all()
    return render_template("get_a_quote.html", policies=insurance_policies)


@app.route("/calculate_quote", methods=["POST"])
def calculate_quote():
    # Retrieve form data
    insurance_policy_id = request.form.get("insurance_policy")
    coverage = float(request.form.get("coverage"))
    deductible = float(request.form.get("deductible"))

    # Find the selected insurance policy
    insurance_policy = Insurance.query.filter_by(policy_id=insurance_policy_id).first()

    if insurance_policy:
        # Retrieve policy details
        premium = insurance_policy.premium

        # Calculate the quote based on coverage and deductible
        quote = premium * (1 + coverage / 100) * (1 - deductible / 100)

        insurance_policies = Insurance.query.all()
        return render_template(
            "get_a_quote.html", policies=insurance_policies, quote=quote
        )
    else:
        return render_template(
            "get_a_quote.html", error="Invalid insurance policy selected"
        )


@app.route("/profile")
def profile():
    # Fetch user data from the database (assuming the user is logged in)
    # Replace this with the actual logic to fetch the logged-in user's data
    user = User.query.get(1)  # Assuming the logged-in user has ID 1
    return render_template("profile.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Query the database to find a user with the provided email and password
        user = User.query.filter_by(Email=email, Password=password).first()

        if user:
            return redirect(url_for("home_page"))
        else:
            return "User not found"
    else:
        return render_template("login.html")


@app.route("/try_again", methods=["POST"])
def try_again():
    user_id = request.form.get("user_id")
    # Retrieve user data based on user_id from the database
    user = User.query.filter_by(id=user_id).first()
    if user:
        if user.Credits > 1:
            # Deduct credits
            user.Credits -= 2
            # Commit the changes to the database
            db.session.commit()
            # Shuffle the cards
            random.shuffle(cards)
            return render_template("index.html", user=user, cards=cards)
        else:
            return "Insufficient credits. Please add more credits to play."
    else:
        return "User not found"  # Handle case where user is not found


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

        # Create a new user instance
        new_user = User(
            Name=first_name,
            Last_name=last_name,
            Date_of_birth=date_of_birth,
            Email=email,
            Password=password,
            Phone_number=phone_number,
            Credits=10,  # Assuming newly registered users get 10 credits
            Street_Address=street_address,
            Zip_code=zip_code,
            Suburb=suburb,
            City=city,
            Country=country,
            sex=gender,
        )

        # Add the new user to the database session and commit
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after successful registration
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


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
    policy = Insurance.query.filter_by(policy_id=policy_id).first()

    if policy:
        policy_dict = policy.to_dict()
        return render_template("policy_details.html", policy=policy_dict)
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
