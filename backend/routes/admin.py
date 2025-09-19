from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from models.user import User

admin_bp = Blueprint("admin_bp", __name__)

# Admin Dashboard
@admin_bp.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only!"}), 403

    return jsonify({"message": "👑 Welcome, Boss Admin!"}), 200


# List all users
@admin_bp.route("/admin/users", methods=["GET"])
@jwt_required()
def list_users():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only!"}), 403

    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "role": u.role}
        for u in users
    ]), 200
