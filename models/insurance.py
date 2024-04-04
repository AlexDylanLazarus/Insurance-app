import uuid
from extensions import db


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
