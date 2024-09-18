"""
Routes for handling cart-related operations.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Product, Cart, CartItem

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart", methods=["GET"])
@jwt_required()
def view_cart():
    """
    Retrieve the current user's cart.

    This endpoint fetches the items in the user's cart and returns them as a JSON object.

    Returns:
        JSON response with the cart items or an empty list if the cart does not exist.
    """
    user = User.query.get(get_jwt_identity())
    cart = user.cart
    if not cart:
        return jsonify({"cart": []}), 200
    cart_items = [
        {
            "product_id": item.product_id,
            "name": item.product.name,
            "quantity": item.quantity,
            "price": item.product.price,
        }
        for item in cart.items
    ]
    return jsonify({"cart": cart_items}), 200


@cart_bp.route("/cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    """
    Add a product to the user's cart.

    This endpoint adds a product to the user's cart. If the cart does not exist, it will be created.
    If the product is already in the cart, its quantity will be updated.

    Returns:
        JSON response with a success message.
    """
    data = request.get_json()
    user = User.query.get(get_jwt_identity())
    cart = user.cart
    if not cart:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
    product = Product.query.get_or_404(data["product_id"])
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += data.get("quantity", 1)
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=data.get(
                "quantity",
                1))
        db.session.add(cart_item)
    db.session.commit()
    return jsonify({"msg": "Product added to cart"}), 200
