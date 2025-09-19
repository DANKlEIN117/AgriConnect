from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

admin_bp = Blueprint("admin", __name__)

# ✅ Admin Dashboard
@admin_bp.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only!"}), 403

    return jsonify({
        "message": "Welcome to the Admin Dashboard 🚀",
        "role": claims["role"]
    }), 200
