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
from flask_wtf import FlaskForm


load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")  # token
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


class PotentialCustomers(db.Model):
    __tablename__ = "potential_customers"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {"id": self.id, "email": self.email}


from cards_bp import cards_bp
from insurance_bp import insurance_bp
from users_bp import users_bp

app.register_blueprint(cards_bp, url_prefix="/cards")
app.register_blueprint(users_bp)
app.register_blueprint(insurance_bp)


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


@app.get("/pol/<int:policy_id>")
def get_policy_page(policy_id):
    policy = Insurance.query.filter_by(policy_id=policy_id).first()

    if policy:
        policy_dict = policy.to_dict()
        return render_template("policy_details.html", policy=policy_dict)
    else:
        return jsonify({"message": "Policy not found"}), 404


@app.route("/profile")
def profile():
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


from wtforms.validators import InputRequired, Length, ValidationError, Email
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField


class RegistrationForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(min=2, max=50)]
    )
    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(min=2, max=50)]
    )
    date_of_birth = DateField(
        "Date of Birth", validators=[InputRequired()], format="%Y-%m-%d"
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    phone_number = StringField(
        "Phone Number", validators=[InputRequired(), Length(min=7, max=15)]
    )
    street_address = StringField(
        "Street Address", validators=[InputRequired(), Length(min=2, max=100)]
    )
    zip_code = StringField(
        "Zip Code", validators=[InputRequired(), Length(min=2, max=20)]
    )
    suburb = StringField("Suburb", validators=[InputRequired(), Length(min=2, max=50)])
    city = StringField("City", validators=[InputRequired(), Length(min=2, max=50)])
    country = StringField(
        "Country", validators=[InputRequired(), Length(min=2, max=50)]
    )
    gender = SelectField(
        "Gender",
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        validators=[InputRequired()],
    )
    submit = SubmitField("Sign Up")

    def validate_email(self, field):
        existing_user = User.query.filter_by(Email=field.data).first()
        if existing_user:
            raise ValidationError("Email is already registered.")

    def validate_phone_number(self, field):
        # Validate phone number format
        if not field.data.isdigit():
            raise ValidationError(
                "Invalid phone number format. Please use digits only."
            )

    def validate_date_of_birth(self, field):
        # Validate age
        from datetime import date

        today = date.today()
        age = (
            today.year
            - field.data.year
            - ((today.month, today.day) < (field.data.month, field.data.day))
        )
        if age < 18:
            raise ValidationError("You must be at least 18 years old to register.")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user instance with form data
        new_user = User(
            Name=form.first_name.data,
            Last_name=form.last_name.data,
            Date_of_birth=form.date_of_birth.data,
            Email=form.email.data,
            Password=form.password.data,
            Phone_number=form.phone_number.data,
            Credits=10,  # Assuming newly registered users get 10 credits
            Street_Address=form.street_address.data,
            Zip_code=form.zip_code.data,
            Suburb=form.suburb.data,
            City=form.city.data,
            Country=form.country.data,
            sex=form.gender.data,
        )

        # Add the new user to the database session and commit
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after successful registration
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
