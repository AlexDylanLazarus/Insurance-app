from flask import Blueprint, render_template, request, jsonify
from models.insurance import Insurance
from models.user import User
from models.cards import cards
from models.potential_customers import PotentialCustomers
from models.userinsurance import UserInsurance
from extensions import db
import random
from .users_bp import LoginForm
from flask_login import login_required, current_user

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/pol")
def pol():
    insurance_policies = Insurance.query.all()
    return render_template("pol.html", policies=insurance_policies)


@main_bp.route("/get_a_quote")
def quote():
    insurance_policies = Insurance.query.all()
    return render_template("get_a_quote.html", policies=insurance_policies)


@main_bp.get("/pol/<int:policy_id>")
def get_policy_page(policy_id):
    policy = Insurance.query.filter_by(policy_id=policy_id).first()

    if policy:
        policy_dict = policy.to_dict()
        return render_template("policy_details.html", policy=policy_dict)
    else:
        return jsonify({"message": "Policy not found"}), 404


@main_bp.route("/profile")
@login_required
def profile():
    # Fetch the current logged-in user
    user = User.query.get(current_user.id)

    # Fetch the policies associated with the current user
    user_policies = [user_insurance.policy for user_insurance in user.user_insurances]

    return render_template(
        "profile.html", user=current_user, user_policies=user_policies
    )


@main_bp.route("/", methods=["GET", "POST"])
@login_required
def home_page():
    return render_template("index.html", user=current_user, cards=cards)


@main_bp.route("/calculate_quote", methods=["POST"])
def calculate_quote():
    # Assuming it's car insurance
    insurance_policy_id = request.form.get("insurance_policy")
    user_age = int(request.form.get("user_age"))
    user_email = request.form.get("user_email")

    # Retrieve the insurance policy based on the provided ID
    insurance_policy = Insurance.query.get(insurance_policy_id)

    if not insurance_policy:
        return render_template("get_a_quote.html", error="Invalid insurance policy ID")

    if insurance_policy.policy_id != 1:
        return render_template(
            "get_a_quote.html", error="Non-car insurance policy selected"
        )

    premium = insurance_policy.premium
    car_year = int(request.form.get("car_year"))
    car_value = float(request.form.get("car_value"))

    # Calculate base quote based on car details
    base_quote = premium * (car_year / 10) * (car_value / 1000)

    # Apply age-based discounts
    if user_age < 25:
        discount = 0.2  # 20% discount for users under 25 years old
    elif user_age >= 25 and user_age < 40:
        discount = 0.1  # 10% discount for users between 25 and 40 years old
    else:
        discount = 0  # No discount for users 40 years old and above

    # Calculate final quote after applying discount
    final_quote = base_quote * (1 - discount)

    # Check if the email already exists in the table
    existing_customer = PotentialCustomers.query.filter_by(email=user_email).first()

    if existing_customer:
        return render_template("get_a_quote.html", quote=final_quote)

    # Save the user's email to the potential customers table
    new_customer = PotentialCustomers(email=user_email)
    db.session.add(new_customer)
    db.session.commit()

    return render_template("get_a_quote.html", quote=final_quote)


@main_bp.route("/try_again", methods=["POST"])
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
            return render_template("index.html", user=current_user, cards=cards)
        else:
            return "Insufficient credits. Please add more credits to play."
    else:
        return "User not found"  # Handle case where user is not found
