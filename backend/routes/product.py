from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.product import Product
from models.user import User

product_bp = Blueprint("product", __name__)

# FARMER adds a product
@product_bp.route("/add", methods=["POST"])
@jwt_required()
def add_product():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != "farmer":
        return jsonify({"error": "Only farmers can add products"}), 403

    data = request.get_json()
    name = data.get("name")
    quantity = data.get("quantity")
    price = data.get("price")

    if not name or not quantity or not price:
        return jsonify({"error": "Missing required fields"}), 400

    product = Product(
        name=name,
        quantity=quantity,
        price=price,
        farmer_id=user.id
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added successfully", "product": product.to_dict()}), 201
