from flask import Blueprint, request, jsonify
from app import db
from models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email") or f"{username}@example.com"
    role = data.get("role", "farmer")  # default role

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if role not in ["farmer", "cooperative", "admin", "buyer"]:
        return jsonify({"error": "Invalid role"}), 400

    # Check duplicates
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create user
    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)  # 🔥 use model method

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "role": role}), 201


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    identifier = data.get("username")  # can be username or email
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"error": "Username/Email and password required"}), 400

    # Try match by username OR email
    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # identity = string, role in claims
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": access_token,
        "role": user.role,
        "username": user.username,
        "email": user.email
    }), 200
