# models.py

'''
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
'''

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    cart = db.relationship('Cart', backref='user', uselist=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    total = db.Column(db.Float, nullable=False)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')