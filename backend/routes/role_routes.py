from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

role_bp = Blueprint("role", __name__)

# Farmer Dashboard
@role_bp.route("/farmer/dashboard", methods=["GET"])
@jwt_required()
def farmer_dashboard():
    claims = get_jwt()
    if claims.get("role") != "farmer":
        return jsonify({"error": "Access forbidden"}), 403
    return jsonify({
        "message": "Welcome to the Farmer Dashboard 🌾",
        "user_id": claims.get("sub")
    }), 200


# Cooperative Dashboard
@role_bp.route("/coop/dashboard", methods=["GET"])
@jwt_required()
def coop_dashboard():
    claims = get_jwt()
    if claims.get("role") != "cooperative":
        return jsonify({"error": "Access forbidden"}), 403
    return jsonify({
        "message": "Welcome to the Cooperative Dashboard 🏢",
        "user_id": claims.get("sub")
    }), 200


# Buyer Dashboard
@role_bp.route("/buyer/dashboard", methods=["GET"])
@jwt_required()
def buyer_dashboard():
    claims = get_jwt()
    if claims.get("role") != "buyer":
        return jsonify({"error": "Access forbidden"}), 403
    return jsonify({
        "message": "Welcome to the Buyer Dashboard 🛒",
        "user_id": claims.get("sub")
    }), 200
