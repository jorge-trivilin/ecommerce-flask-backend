"""
orders.py

This module defines the routes for handling order-related operations
in the e-commerce application. It provides endpoints for placing orders,
retrieving order history, and fetching details of specific orders.

Main Functionality:
- Place an order based on the current user's cart.
- Retrieve the current user's order history, sorted from most recent to oldest.
- Get detailed information about a specific order, including all items in the order.

Endpoints:
- POST /orders: Places an order for items in the user's cart.
  Returns a success message and the order ID if successful,
  or an error message if the cart is empty.

- GET /orders/history: Retrieves a list of all orders made by the current user.
  Returns a JSON response containing the user's order list.

- GET /orders/<int:order_id>: Retrieves detailed information about a specific order.
  Requires the order ID as a parameter and returns the order details.

Usage:
To use this module, it should be registered with a Flask application instance
to enable the defined routes.

Example:
    from app.routes.orders import orders_bp

    app.register_blueprint(orders_bp)

"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, CartItem, Order, OrderItem

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("", methods=["POST"])
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
    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()

    return jsonify({"msg": "Order placed successfully", "order_id": order.id}), 201


@orders_bp.route("/history", methods=["GET"])
@jwt_required()
def get_order_history():
    """
    Retrieve the current user's order history.

    This endpoint returns a list of all orders made by the user,
    sorted from the most recent to the oldest.

    Returns:
        JSON response containing the user's order list.
    """
    user = User.query.get(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.id.desc()).all()

    order_history = [
        {
            "id": order.id,
            "total": order.total,
            "date": order.date.isoformat() if hasattr(order, "date") else None,
            "items_count": len(order.order_items),
        }
        for order in orders
    ]

    return jsonify({"orders": order_history}), 200


@orders_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order_details(order_id):
    """
    Recupera os detalhes de um pedido específico.

    Este endpoint retorna informações detalhadas sobre um pedido,
    incluindo todos os itens do pedido.

    Args:
        order_id (int): O ID do pedido a ser visualizado.

    Returns:
        JSON response com os detalhes do pedido.
    """
    user = User.query.get(get_jwt_identity())
    order = Order.query.filter_by(id=order_id, user_id=user.id).first()

    if not order:
        return jsonify({"msg": "Pedido não encontrado"}), 404

    order_items = [
        {
            "product_id": item.product_id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": item.price,
        }
        for item in order.order_items
    ]

    order_details = {
        "id": order.id,
        "total": order.total,
        "date": order.date.isoformat() if hasattr(order, "date") else None,
        "items": order_items,
    }

    return jsonify({"order": order_details}), 200
