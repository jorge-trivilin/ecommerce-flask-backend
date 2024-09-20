"""
cart_service.py: SQLAlchemy Implementation for Cart Management

This module provides an implementation of shopping cart management services using SQLAlchemy.
It includes the `SQLAlchemyCartService` class, which adheres to the `CartServiceProtocol` and
offers various operations to manage user carts in a relational database.

Protocols:
    - CartServiceProtocol: A protocol for defining cart-related services.

Classes:
    - SQLAlchemyCartService: A concrete implementation of the CartServiceProtocol for managing
      shopping carts using SQLAlchemy.

Detailed Description:
    1. SQLAlchemyCartService Class:
       Implements the CartServiceProtocol with SQLAlchemy.
       Methods:
       - add_item(user_id: int, product_id: int, quantity: int) -> None:
         Adds a product to the specified user's cart. If the cart does not exist, a new one is
         created. Updates the quantity of the product if it is already present in the cart;
         otherwise, adds a new item.
       - remove_item(user_id: int, product_id: int) -> None:
         Removes a product from the specified user's cart. Raises a ValueError if the cart or item
         is not found.
       - get_cart(user_id: int) -> List[CartItem]:
         Retrieves all items from the user's cart. Returns an empty list if the cart does not
         exist.
       - clear_cart(user_id: int) -> None:
         Clears all items from the user's cart. The cart is emptied, and changes are committed
         to the database.

Usage:
    - Implement the CartServiceProtocol to provide a concrete service for managing cart operations.
    - Use SQLAlchemyCartService to handle cart management in a SQLAlchemy-based application.

This module enhances the management of shopping carts by integrating SQLAlchemy for database
operations, ensuring robust and reliable cart functionalities within the application.
"""
from typing import List
from app.protocols import CartServiceProtocol, CartItem, ConcreteCartItem
from app.models import db, Cart, CartItem as CartItemModel


class SQLAlchemyCartService(CartServiceProtocol):
    """
    A service class for managing shopping cart operations using SQLAlchemy.

    This class implements the CartServiceProtocol and provides methods to
    add, remove, view, and clear items in a user's shopping cart. It interacts
    with the database using SQLAlchemy models.

    Methods:
        add_item(user_id: int, product_id: int, quantity: int) -> None:
            Adds a product to the cart for the specified user. If the cart or
            the cart item does not exist, they are created. If the item already
            exists in the cart, its quantity is updated.

        remove_item(user_id: int, product_id: int) -> None:
            Removes a product from the cart for the specified user. Raises a
            ValueError if the cart or the item does not exist.

        get_cart(user_id: int) -> List[CartItem]:
            Retrieves all items in the cart for the specified user. Returns
            an empty list if the cart does not exist.

        clear_cart(user_id: int) -> None:
            Removes all items from the cart for the specified user. The cart
            itself is not deleted.

    Raises:
        ValueError: If the cart or item does not exist when attempting to
                    remove an item.
    """

    def add_item(self, user_id: int, product_id: int, quantity: int) -> None:
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)

        cart_item = CartItemModel.query.filter_by(
            cart_id=cart.id, product_id=product_id
        ).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItemModel(
                cart_id=cart.id, product_id=product_id, quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()

    def remove_item(self, user_id: int, product_id: int) -> None:
        # cart = Cart.query.filter_by(user_id=user_id).first()
        # if cart:
        #     CartItemModel.query.filter_by(cart_id=cart.id, product_id=product_id).delete()
        #     db.session.commit()

        # Find the cart for the given user
        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            raise ValueError("Cart not found")

        # Find the cart item for the given product_id
        cart_item = CartItemModel.query.filter_by(
            cart_id=cart.id, product_id=product_id
        ).first()

        if not cart_item:
            raise ValueError("Item not found in cart")

        # Remove the cart item if found
        db.session.delete(cart_item)
        db.session.commit()

    def get_cart(self, user_id: int) -> List[CartItem]:
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            return []
        return [
            ConcreteCartItem(product_id=item.product_id, quantity=item.quantity)
            for item in cart.items
        ]

    def clear_cart(self, user_id: int) -> None:
        cart = Cart.query.filter_by(user_id=user_id).first()
        if cart:
            CartItemModel.query.filter_by(cart_id=cart.id).delete()
            db.session.commit()
