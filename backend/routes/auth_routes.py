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
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "farmer")  # default farmer

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        username=username,
        email=email,
        role=role
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"{role.capitalize()} registered successfully"}), 201


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify({"access_token": access_token, "role": user.role}), 200
