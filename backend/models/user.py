from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="farmer")  
    # roles: farmer, cooperative, buyer, admin

    # relationships
    farmer = db.relationship("Farmer", backref="user", uselist=False)
    cooperative = db.relationship("Cooperative", backref="user", uselist=False)
    buyer = db.relationship("Buyer", backref="user", uselist=False)

    def set_password(self, password):
        """Hash the password before saving"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify hashed password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
