import uuid
from extensions import db


class PotentialCustomers(db.Model):
    __tablename__ = "potential_customers"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {"id": self.id, "email": self.email}
