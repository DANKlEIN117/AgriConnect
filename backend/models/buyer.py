from app import db

class Buyer(db.Model):
    __tablename__ = "buyers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    company_name = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"<Buyer {self.company_name}>"
