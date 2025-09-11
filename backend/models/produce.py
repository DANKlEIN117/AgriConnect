from app import db

class Produce(db.Model):
    __tablename__ = "produce"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g. maize, milk
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)

    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id"), nullable=False)
    cooperative_id = db.Column(db.Integer, db.ForeignKey("cooperatives.id"), nullable=True)

    def __repr__(self):
        return f"<Produce {self.name} - {self.quantity}>"
