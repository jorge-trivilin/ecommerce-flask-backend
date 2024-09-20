"""
models.py: Database Models for E-commerce Backend

This module defines the database schema for a simple e-commerce platform using SQLAlchemy ORM.
It includes models for users, products, shopping carts, and orders, establishing the necessary
relationships between these entities.

Models:
    User: Represents registered users of the platform.
    Product: Represents products available for purchase.
    Cart: Represents a user's shopping cart.
    CartItem: Represents individual items in a user's cart.
    Order: Represents a completed order.
    OrderItem: Represents individual items in a completed order.

Each model is defined as a SQLAlchemy Model class, with appropriate fields and relationships.
The User model includes methods for password hashing and verification to ensure secure
authentication.

Relationships:
    - User to Cart: One-to-One
    - User to Order: One-to-Many
    - Cart to CartItem: One-to-Many
    - Order to OrderItem: One-to-Many
    - Product to CartItem: One-to-Many
    - Product to OrderItem: One-to-Many

Usage:
    This module should be imported and used in conjunction with Flask-SQLAlchemy to set up
    the database and perform operations on the defined models.

Note:
    Ensure that you initialize and configure SQLAlchemy with your Flask application before
    using these models.
"""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import String, Boolean, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model):  # type: ignore
    """
    Represents a registered user in the system.

    Attributes:
        id: The unique identifier for the user.
        username: The username of the user.
        email: The email address of the user.
        password_hash: The hashed password of the user.
        is_admin: A boolean indicating if the user is an admin.
        cart: The user's shopping cart (one-to-one relationship).
        orders: The orders placed by the user (one-to-many relationship).
    """

    # id = Column(Integer, primary_key=True)
    # username = Column(String(80), unique=True, nullabe=False)
    # email = Column(String(120), unique=True, nullabe=False)
    # password_hash = Column(String(128), nullable=False)
    # is_admin = Column(Boolean, default=False)
    # cart = relationship("Cart", back_populates="user", uselist=False)
    # orders = relationship("Order", back_populates="user")
    # --
    # based on https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    cart: Mapped[Optional["Cart"]] = relationship(
        "Cart", back_populates="user", uselist=False
    )
    orders: Mapped[List["Order"]] = relationship(
        "Order", back_populates="user")

    def set_password(self, password: str) -> None:
        """
        Sets the hashed password for the user.

        Args:
            password: The plain-text password to hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the hashed password.

        Args:
            password: The plain-text password to check.

        Returns:
            True if the password is correct, False otherwise.
        """
        # Checks if pwhash is valid before checking for the password
        if self.password_hash is None:
            return False  # Returns false if the password has is not defined
        # Verification is useful to prevent errors in cases where a user does not
        # have a defined password hash or in incorrect object initialization
        # scenarios.
        return check_password_hash(self.password_hash, password)


class Product(db.Model):  # type: ignore
    """
    Represents a product available for purchase.

    Attributes:
        id: The unique identifier for the product.
        name: The name of the product.
        description: A description of the product.
        price: The price of the product.
        stock: The quantity of the product in stock.
    """

    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(default=0)


class Cart(db.Model):  # type: ignore
    """
    Represents a user's shopping cart.

    Attributes:
        id: The unique identifier for the cart.
        user_id: The identifier of the user who owns the cart.
        user: The user associated with the cart (one-to-one relationship).
        items: The items in the cart (one-to-many relationship).
    """

    __tablename__ = "cart"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="cart")
    items: Mapped[List["CartItem"]] = relationship(
        "CartItem", back_populates="cart")


class CartItem(db.Model):  # type: ignore
    """
    Represents an item in a shopping cart.

    Attributes:
        id: The unique identifier for the cart item.
        cart_id: The identifier of the cart to which the item belongs.
        product_id: The identifier of the product.
        quantity: The quantity of the product in the cart.
        cart: The cart associated with the item (one-to-one relationship).
        product: The product associated with the item (one-to-one relationship).
    """

    __tablename__ = "cart_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship("Product")


class Order(db.Model):  # type: ignore
    """
    Represents a completed order.

    Attributes:
        id: The unique identifier for the order.
        user_id: The identifier of the user who placed the order.
        total: The total amount of the order.
        date: The date and time when the order was placed.
        user: The user who placed the order (one-to-one relationship).
        order_items: The items in the order (one-to-many relationship).
    """

    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    # date: Mapped[datetime] = mapped_column(
    # default=datetime.utcnow, nullable=False)
    date: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="orders")
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="order"
    )


class OrderItem(db.Model):  # type: ignore
    """
    Represents an item in a completed order.

    Attributes:
        id: The unique identifier for the order item.
        order_id: The identifier of the order to which the item belongs.
        product_id: The identifier of the product.
        quantity: The quantity of the product in the order.
        price: The price of the product at the time of the order.
        order: The order associated with the item (one-to-one relationship).
        product: The product associated with the item (one-to-one relationship).
    """

    __tablename__ = "order_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    order: Mapped["Order"] = relationship(
        "Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product")
