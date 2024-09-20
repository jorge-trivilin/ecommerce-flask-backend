"""
cart.py: Cart Management Routes for E-Commerce Platform

This module defines Flask routes for managing a user's shopping cart in an e-commerce platform.
It provides endpoints to view, add, remove, and clear items in the user's cart.

Endpoints:
    - GET /cart: Retrieve the current user's cart contents.
    - POST /cart: Add a product to the user's cart or update its quantity.
    - DELETE /cart/<product_id>: Remove a specific product from the user's cart.
    - DELETE /cart/clear: Clear all items from the user's cart.

Functions:
    - view_cart(): Retrieves and returns the contents of the current user's cart.
    - add_to_cart(): Adds a product to the user's cart or updates its quantity if already present.
    - remove_from_cart(product_id): Removes a specific product from the user's cart.
    - clear_cart(): Clears all items from the user's cart.

Authentication:
    All endpoints require JWT authentication to ensure that operations are performed by the
    authenticated user.

Error Handling:
    The module includes error handling for:
    - Attempting to access or modify a non-existent cart.
    - Trying to remove an item that's not present in the cart.

Dependencies:
    - Flask: The web framework used for building the API.
    - Flask-JWT-Extended: Provides JSON Web Tokens (JWT) for authentication.
    - SQLAlchemy: Used for ORM and database interactions via the `app.models` module.

Models Used:
    - User: Represents the authenticated user.
    - Cart: Manages the user's shopping cart.
    - CartItem: Handles individual items within the cart.
    - Product: References products added to the cart.

Notes:
    - This module assumes that a user can only have one active cart at any given time.
    - Operations are delegated to the `SQLAlchemyCartService` class for cart management logic.

This module integrates with SQLAlchemy and JWT for secure and efficient cart management, providing
a comprehensive API for shopping cart operations within the application.
"""


from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# from app.models import db, User, Product, Cart, CartItem
from app.cart_service import SQLAlchemyCartService

cart_bp = Blueprint("cart_bp", __name__, url_prefix="/cart")
cart_service = SQLAlchemyCartService()


@cart_bp.route("", methods=["GET"])
@jwt_required()
def view_cart():
    """
    Retrieve the current user's cart.

    This endpoint fetches the items in the user's cart and returns them as a JSON object.

    Returns:
        JSON response with the cart items or an empty list if the cart does not exist.
    """
    # user = User.query.get(get_jwt_identity())
    # cart = user.cart
    # if not cart:
    #     return jsonify({"cart": []}), 200
    # cart_items = [
    #     {
    #         "product_id": item.product_id,
    #         "name": item.product.name,
    #         "quantity": item.quantity,
    #         "price": item.product.price,
    #     }
    #     for item in cart.items
    # ]
    # return jsonify({"cart": cart_items}), 200

    user_id = get_jwt_identity()
    cart_items = cart_service.get_cart(user_id)

    # Converting ConcreteCartItem object to dictionaries for JSON serialization
    serialized_cart_items = [
        {"product_id": item.product_id, "quantity": item.quantity}
        for item in cart_items
    ]

    return jsonify({"cart": serialized_cart_items}), 200


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
    # -- Legacy --
    # data = request.get_json()
    # user = User.query.get(get_jwt_identity())
    # cart = user.cart
    # if not cart:
    #     cart = Cart(user_id=user.id)
    #     db.session.add(cart)
    #     db.session.commit()
    # product = Product.query.get_or_404(data["product_id"])
    # cart_item = CartItem.query.filter_by(
    #     cart_id=cart.id, product_id=product.id).first()
    # if cart_item:
    #     cart_item.quantity += data.get("quantity", 1)
    # else:
    #     cart_item = CartItem(
    #         cart_id=cart.id,
    #         product_id=product.id,
    #         quantity=data.get(
    #             "quantity",
    #             1))
    #     db.session.add(cart_item)
    # db.session.commit()

    data = request.get_json()
    # Fetching user ID from JWT token
    user_id = get_jwt_identity()
    # Getting product_id and quantity from the request data
    product_id = data["product_id"]
    quantity = data.get("quantity", 1)  # Default to 1 if not provided
    # Delegating cart logic to the cart_service
    cart_service.add_item(user_id=user_id, product_id=product_id, quantity=quantity)
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
    # user = User.query.get(get_jwt_identity())
    # cart = user.cart

    # if not cart:
    #     return jsonify({"msg": "Cart not found"}), 404

    # cart_item = CartItem.query.filter_by(
    #     cart_id=cart.id, product_id=product_id).first()

    # if not cart_item:
    #     return jsonify({"msg": "Item not found in cart"}), 404

    # db.session.delete(cart_item)
    # db.session.commit()

    # return jsonify({"msg": "Item successfully removed from cart"}), 200

    # Get the current user's ID from the JWT token
    user_id = get_jwt_identity()

    try:
        # Delegate cart removal logic to the cart_service
        cart_service.remove_item(user_id=user_id, product_id=product_id)
        return jsonify({"msg": "Item successfully removed from cart"}), 200

    except ValueError as e:
        # If the cart or item isn't found, return an appropriate error
        return jsonify({"msg": str(e)}), 404


@cart_bp.route("/clear", methods=["DELETE"])
@jwt_required()
def clear_cart():
    """
    Clear the user's entire cart.
    """
    user_id = get_jwt_identity()
    cart_service.clear_cart(user_id)
    return jsonify({"msg": "Cart cleared"}), 200
