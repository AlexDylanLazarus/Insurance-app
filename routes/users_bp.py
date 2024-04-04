from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from models.user import User
from extensions import db
from wtforms.validators import InputRequired, Length, ValidationError, Email
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from flask_wtf import FlaskForm
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users_bp", __name__)


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


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Login")

    # Custom validation for email
    def validate_email(self, field):
        user = User.query.filter_by(Email=field.data).first()
        if not user:
            raise ValidationError("Invalid email address")

    # Custom validation for password
    def validate_password(self, field):
        user = User.query.filter_by(Email=self.email.data).first()
        if user:
            user_data_db = user.to_dict()
            form_password = field.data
            if not check_password_hash(user_data_db["Password"], form_password):
                raise ValidationError("Invalid password")


@users_bp.route("/users", methods=["POST"])
def post_user():
    new_user_data = request.json
    new_user = User(**new_user_data)
    db.session.add(new_user)
    db.session.commit()
    result = {"message": "User Added Successfully"}
    return jsonify(result), 201


@users_bp.route("/users/<id>")
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({"message": "User not found"}), 404


@users_bp.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return (
            jsonify({"message": "User deleted successfully", "data": user.to_dict()}),
            200,
        )
    else:
        return jsonify({"message": "User not found"}), 404


@users_bp.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user_data = request.json
    user = User.query.get(id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.session.commit()
        return (
            jsonify({"message": "User updated successfully", "data": user.to_dict()}),
            200,
        )
    else:
        return jsonify({"message": "User not found"}), 404


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Query the database to find a user with the provided email and password
        user = User.query.filter_by(Email=email).first()
        if user:
            login_user(user)  # Ensure login_user() is called before redirect
            # Redirect to home page upon successful login
            return redirect(url_for("main_bp.home_page"))
        else:
            # Render the login page with an error message
            return render_template("login.html", form=form, error="User not found")
    return render_template("login.html", form=form)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user instance with form data
        password_hash = generate_password_hash(form.password.data)
        new_user = User(
            Name=form.first_name.data,
            Last_name=form.last_name.data,
            Date_of_birth=form.date_of_birth.data,
            Email=form.email.data,
            Password=password_hash,
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
        return redirect(url_for("users_bp.login"))
    return render_template("register.html", form=form)
