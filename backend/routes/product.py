from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from models.product import Product
from models.user import User
from datetime import datetime

product_bp = Blueprint("products", __name__)

# Add Product (farmer only)
@product_bp.route("/", methods=["POST"])
@jwt_required()
def add_product():
    claims = get_jwt()
    if claims.get("role") != "farmer":
        return jsonify({"error": "Only farmers can add products"}), 403

    data = request.get_json()
    name = data.get("name")
    quantity = data.get("quantity")
    price = data.get("price")
    due_date = data.get("due_date")
    status = data.get("status", "available")

    product = Product(
        name=name,
        quantity=quantity,
        price=price,
        due_date=datetime.fromisoformat(due_date) if due_date else None,
        status=status,
        farmer_id=get_jwt_identity()
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added successfully!"}), 201


# Admin view all products
@product_bp.route("/all", methods=["GET"])
@jwt_required()
def view_all_products():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only!"}), 403

    products = Product.query.all()
    results = []
    for p in products:
        prod_dict = p.to_dict()
        farmer = User.query.get(p.farmer_id)
        prod_dict["farmer_username"] = farmer.username if farmer else None
        results.append(prod_dict)

    return jsonify({"products": results}), 200


# Farmer view their products
@product_bp.route("/mine", methods=["GET"])
@jwt_required()
def view_my_products():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != "farmer":
        return jsonify({"error": "Only farmers can view their products"}), 403

    products = Product.query.filter_by(farmer_id=user.id).all()
    results = [p.to_dict() for p in products]

    return jsonify({"my_products": results}), 200


# Cooperative view all products
@product_bp.route("/cooperative", methods=["GET"])
@jwt_required()
def cooperative_view_products():
    claims = get_jwt()
    if claims.get("role") != "cooperative":
        return jsonify({"error": "Only cooperatives can view this"}), 403

    products = Product.query.all()
    results = []
    for p in products:
        prod_dict = p.to_dict()
        farmer = User.query.get(p.farmer_id)
        prod_dict["farmer_username"] = farmer.username if farmer else None
        results.append(prod_dict)

    return jsonify({"products": results}), 200


# Edit product
@product_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def edit_product(product_id):
    claims = get_jwt()
    user_id = get_jwt_identity()

    product = Product.query.get_or_404(product_id)

    if claims.get("role") != "farmer" or product.farmer_id != int(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    product.name = data.get("name", product.name)
    product.quantity = data.get("quantity", product.quantity)
    product.price = data.get("price", product.price)
    product.status = data.get("status", product.status)

    if "due_date" in data:
        product.due_date = datetime.fromisoformat(data["due_date"])

    db.session.commit()
    return jsonify({"message": "Product updated successfully!"}), 200


# Delete product
@product_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    claims = get_jwt()
    user_id = get_jwt_identity()

    product = Product.query.get_or_404(product_id)

    if claims.get("role") != "farmer" or product.farmer_id != int(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"}), 200


# Public + Filtered view
@product_bp.route("/", methods=["GET"])
@jwt_required(optional=True)
def get_products():
    query = Product.query

    name = request.args.get("name")
    status = request.args.get("status")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if status:
        query = query.filter_by(status=status)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "price": p.price,
            "status": p.status,
            "farmer_id": p.farmer_id
        } for p in products
    ])
