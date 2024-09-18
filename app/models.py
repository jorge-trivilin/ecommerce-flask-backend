# models.py

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
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Boolean, Text, Float, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Optional

db: SQLAlchemy = SQLAlchemy() 

class User(db.Model): # type: ignore
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    cart: Mapped[Optional["Cart"]] = relationship("Cart", back_populates="user", uselist=False)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Product(db.Model): # type: ignore
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(default=0)


class Cart(db.Model): # type: ignore
    __tablename__ = 'cart'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="cart")
    items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="cart")


class CartItem(db.Model): # type: ignore
    __tablename__ = 'cart_item'
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship("Product")


class Order(db.Model): # type: ignore
    __tablename__ = 'order'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="orders")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")

class OrderItem(db.Model): # type: ignore
    __tablename__ = 'order_item'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product")