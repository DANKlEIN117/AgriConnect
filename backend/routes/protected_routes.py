from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

protected_bp = Blueprint("protected", __name__)

@protected_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    claims = get_jwt()
    return jsonify({
        "message": "✅ You accessed a protected route",
        "role": claims.get("role")
    }), 200
