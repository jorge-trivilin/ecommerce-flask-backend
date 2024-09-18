"""
__init__.py

This module initializes the routing for the e-commerce Flask application by
creating and registering Blueprints for different functionalities. It serves
as the main entry point for defining application routes.

Blueprints:
- auth_bp: Handles user authentication routes, including registration and login.
- products_bp: Manages product-related routes, such as retrieving, adding,
  editing, and deleting products.

Main Functionality:
- The routes are registered under specific URL prefixes to organize the API
  structure:
  - Authentication routes are available under the prefix `/api/auth`.
  - Product management routes are available under the prefix `/api/products`.

Usage:
This module should be imported in the main application file to ensure that
the routes are properly registered and accessible.

Example:
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

"""

# app/routes/__init__.py

from flask import Blueprint
from .auth import auth_bp
from .products import products_bp

# from .orders import orders_bp
from .cart import cart_bp

# Main Blueprint creation for routes
routes_bp = Blueprint("routes", __name__)

routes_bp.register_blueprint(auth_bp, url_prefix="/auth")
routes_bp.register_blueprint(products_bp)
# routes_bp.register_blueprint(orders_bp)
routes_bp.register_blueprint(cart_bp)
