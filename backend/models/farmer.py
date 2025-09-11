from app import db

class Farmer(db.Model):
    __tablename__ = "farmers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    location = db.Column(db.String(120), nullable=True)
    farm_type = db.Column(db.String(100), nullable=True)  # e.g. maize, livestock
    produce = db.relationship("Produce", backref="farmer", lazy=True)

    def __repr__(self):
        return f"<Farmer {self.user_id} - {self.farm_type}>"
