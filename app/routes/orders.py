"""
Routes for handling order-related operations.
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Cart, Order, OrderItem

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["POST"])
@jwt_required()
def place_order():
    """
    Place an order based on the current user's cart.

    This endpoint processes the items in the user's cart, creates an order,
    and clears the cart after successfully placing the order.

    Returns:
        JSON response with a success message and the order ID if successful,
        or an error message if the cart is empty.
    """
    user = User.query.get(get_jwt_identity())
    cart = user.cart

    if not cart or not cart.items:
        return jsonify({"msg": "Cart is empty"}), 400

    total = sum(item.product.price * item.quantity for item in cart.items)
    order = Order(user_id=user.id, total=total)
    db.session.add(order)
    db.session.commit()

    for item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price,
        )
        db.session.add(order_item)
    db.session.commit()

    # Clear the cart
    Cart.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()

    return jsonify({"msg": "Order placed successfully",
                   "order_id": order.id}), 201
