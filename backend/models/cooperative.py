from app import db

class Cooperative(db.Model):
    __tablename__ = "cooperatives"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=True)
    products = db.relationship("Produce", backref="cooperative", lazy=True)

    def __repr__(self):
        return f"<Cooperative {self.name}>"
