import uuid
from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
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
