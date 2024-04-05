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
from flask_wtf import FlaskForm
from flask_login import LoginManager
from extensions import db
from models.user import User


load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")  # token
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
# db = SQLAlchemy(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # db.create_all()
except Exception as e:
    print("Error connecting to the database:", e)


from routes.cards_bp import cards_bp
from routes.insurance_bp import insurance_bp
from routes.users_bp import users_bp
from routes.main_bp import main_bp
from routes.potential_bp import potential_bp
from routes.userinsurance_bp import userinsurance_bp

app.register_blueprint(cards_bp, url_prefix="/cards")
app.register_blueprint(users_bp)
app.register_blueprint(insurance_bp)
app.register_blueprint(main_bp)
app.register_blueprint(potential_bp, url_prefix="/potential")
app.register_blueprint(userinsurance_bp, url_prefix="/userinsurance")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
