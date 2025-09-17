from app import db

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coop_id = db.Column(db.Integer, nullable=False)  # Cooperative user id
    produce_id = db.Column(db.Integer, db.ForeignKey("produce.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, accepted, rejected
