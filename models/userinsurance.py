from extensions import db
from models.insurance import Insurance  # Import the Insurance model


class UserInsurance(db.Model):
    __tablename__ = "user_insurance"

    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), primary_key=True)
    policy_id = db.Column(
        db.Integer, db.ForeignKey("insurance_policies.policy_id"), primary_key=True
    )

    # Define relationships
    user = db.relationship("User", back_populates="user_insurances")
    policy = db.relationship(
        "Insurance", back_populates="user_insurances"
    )  # Use Insurance model here

    # JSON serialization
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "policy_id": self.policy_id,
            # Add any other fields you want to include in the JSON representation
        }
