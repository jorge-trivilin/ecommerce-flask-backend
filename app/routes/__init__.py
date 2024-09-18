# app/routes/__init__.py

from flask import Blueprint

# Import Blueprints
from .auth import auth_bp
from .products import products_bp

# Main Blueprint creation for routes
routes_bp = Blueprint('routes', __name__)

# Blueprint registrations inside main Blueprint
routes_bp.register_blueprint(auth_bp, url_prefix='/api/auth')
routes_bp.register_blueprint(products_bp, url_prefix='/api/products')
