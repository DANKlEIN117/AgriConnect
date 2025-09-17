from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from models.produce import Produce
from models.request import Request


produce_bp = Blueprint("produce", __name__)

@produce_bp.route("/produce", methods=["POST"])
@jwt_required()
def create_produce():
    # ✅ extract identity & role from token
    user_id = int(get_jwt_identity())  
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

@produce_bp.route("/produce", methods=["GET"])
@jwt_required()
def get_produce():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get("role")

    # Farmers see only their produce
    if role == "farmer":
        produce = Produce.query.filter_by(farmer_id=user_id).all()
    else:
        # Cooperatives or admins can see all produce
        produce = Produce.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "price": p.price,
            "farmer_id": p.farmer_id
        } for p in produce
    ])
@produce_bp.route("/produce/<int:produce_id>", methods=["PUT"])
@jwt_required()
def update_produce(produce_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get("role")

    data = request.get_json()
    produce = Produce.query.get_or_404(produce_id)

    # Farmers can only edit their own produce
    if role == "farmer" and produce.farmer_id != user_id:
        return jsonify({"message": "Not authorized to edit this produce"}), 403

    # Update fields if provided
    produce.name = data.get("name", produce.name)
    produce.quantity = data.get("quantity", produce.quantity)
    produce.price = data.get("price", produce.price)

    db.session.commit()
    return jsonify({"message": "Produce updated successfully"})


@produce_bp.route("/produce/<int:produce_id>", methods=["DELETE"])
@jwt_required()
def delete_produce(produce_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get("role")

    produce = Produce.query.get_or_404(produce_id)

    # Farmers can only delete their own produce
    if role == "farmer" and produce.farmer_id != user_id:
        return jsonify({"message": "Not authorized to delete this produce"}), 403

    db.session.delete(produce)
    db.session.commit()
    return jsonify({"message": "Produce deleted successfully"})


@produce_bp.route("/produce/all", methods=["GET"])
@jwt_required()
def get_all_produce():
    claims = get_jwt()
    role = claims.get("role")

    if role not in ["cooperative", "admin"]:
        return jsonify({"message": "Not authorized"}), 403

    produce = Produce.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "price": p.price,
            "farmer_id": p.farmer_id
        } for p in produce
    ])

@produce_bp.route("/produce/<int:produce_id>/request", methods=["POST"])
@jwt_required()
def request_produce(produce_id):
    claims = get_jwt()
    role = claims.get("role")
    coop_id = int(get_jwt_identity())

    if role != "cooperative":
        return jsonify({"message": "Only cooperatives can request produce"}), 403

    data = request.get_json()
    quantity = data.get("quantity")

    if not quantity:
        return jsonify({"error": "Quantity is required"}), 400

    new_request = Request(
        coop_id=coop_id,
        produce_id=produce_id,
        quantity=quantity
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Request submitted successfully"}), 201

@produce_bp.route("/requests", methods=["GET"])
@jwt_required()
def get_requests():
    claims = get_jwt()
    role = claims.get("role")
    user_id = int(get_jwt_identity())

    if role == "cooperative":
        # Only see their own requests
        requests = Request.query.filter_by(coop_id=user_id).all()
    elif role == "admin":
        # Admin sees all requests
        requests = Request.query.all()
    else:
        return jsonify({"message": "Not authorized"}), 403

    return jsonify([
        {
            "id": r.id,
            "produce_id": r.produce_id,
            "quantity": r.quantity,
            "status": r.status
        } for r in requests
    ])

