from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import Blueprint, request, jsonify
from app import db
from models.produce import Produce

produce_bp = Blueprint("produce", __name__)

@produce_bp.route("/produce", methods=["POST"])
@jwt_required()
def create_produce():
    user_id = int(get_jwt_identity())  # cast back to int
    claims = get_jwt()
    role = claims.get("role")

    if role != "farmer":
        return jsonify({"error": "Only farmers can add produce"}), 403

    data = request.get_json()
    produce = Produce(
        name=data["name"],
        quantity=data["quantity"],
        price=data.get("price"),
        farmer_id=user_id
    )
    db.session.add(produce)
    db.session.commit()

    return jsonify({"message": "Produce added successfully"}), 201
