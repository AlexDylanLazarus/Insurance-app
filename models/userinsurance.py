from extensions import db


class UserInsurance(db.Model):
    __tablename__ = "user_insurance"

    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), primary_key=True)
    policy_id = db.Column(
        db.Integer, db.ForeignKey("insurance_policies.policy_id"), primary_key=True
    )

    user = db.relationship("User", back_populates="user_insurances")
    policy = db.relationship("Insurance", back_populates="user_insurances")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "policy_id": self.policy_id,
        }
