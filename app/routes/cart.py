"""
Routes for handling cart-related operations.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Product, Cart, CartItem

cart_bp = Blueprint("cart_bp", __name__, url_prefix="/api/cart")


@cart_bp.route("", methods=["GET"])
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


@cart_bp.route("", methods=["POST"])
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


@cart_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(product_id):
    """
    Remove an item from the user's cart.

    This endpoint removes a specific product from the current user's cart.
    If the item is not in the cart, it returns an error message.

    Args:
        product_id (int): The ID of the product to be removed from the cart.

    Returns:
        JSON response with a success or error message.
    """
    user = User.query.get(get_jwt_identity())
    cart = user.cart

    if not cart:
        return jsonify({"msg": "Cart not found"}), 404

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id, product_id=product_id).first()

    if not cart_item:
        return jsonify({"msg": "Item not found in cart"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"msg": "Item successfully removed from cart"}), 200
