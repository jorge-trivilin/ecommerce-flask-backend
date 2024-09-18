# products.py

"""
auth.py

This module handles user authentication for the e-commerce platform using Flask.
It provides endpoints for user registration and login, allowing users to create
accounts and access the system securely. The module ensures that usernames and
emails are unique, and that passwords are stored securely.

Endpoints:
- POST /register: Allows a new user to register by providing a username, email,
  and password. It checks for the uniqueness of the username and email before
  creating an account.
  
- POST /login: Allows an existing user to log in by providing their username
  and password. If the credentials are valid, an access token is generated
  and returned.

Functions:
- admin_required(fn): A decorator that checks if the current user has admin
  privileges before allowing access to certain endpoints.
  
- get_products(): Retrieves a list of all products in the database.
  
- get_product(product_id): Retrieves detailed information about a specific product
  identified by its product ID.
  
- add_product(): Allows an admin user to add a new product to the database,
  requiring name and price as mandatory fields.
  
- edit_product(product_id): Allows an admin user to update the details of an
  existing product identified by its product ID.
  
- delete_product(product_id): Allows an admin user to delete a product from
  the database identified by its product ID.

Error Handling:
The module includes error handling for various scenarios such as:
- Checking for required fields during product addition.
- Handling exceptions during database operations.
- Returning appropriate HTTP status codes and messages for errors.

Dependencies:
- Flask: Web framework used for building the API.
- Flask-JWT-Extended: Library used for handling JSON Web Tokens (JWT) for authentication.
- SQLAlchemy: ORM used for database interactions.

"""

from flask import Blueprint, request, jsonify
from app.models import db, Product, User
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from functools import wraps

products_bp = Blueprint('products', __name__)

# Decorator to check for admin privileges
def admin_required(fn):
    """
    Decorator to check for admin privileges.
    
    This decorator verifies that the request contains a valid JWT token
    and that the user associated with the token has admin privileges.
    
    Args:
        fn (callable): The function to be decorated.
    
    Returns:
        callable: The wrapped function that checks for admin privileges.
    
    Raises:
        HTTPException: 403 Forbidden if the user is not an admin.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({"msg": "Admin privilege required"}), 403
        return fn(*args, **kwargs)
    return wrapper

@products_bp.route('/products', methods=['GET'])
def get_products():
    """
    Retrieve all products.
    
    This function queries the database for all products and returns them as a JSON array.
    
    Returns:
        tuple: A tuple containing:
            - A JSON array of all products with their details.
            - HTTP status code 200.
    """
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock
        } for p in products
    ]), 200

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Retrieve a specific product by its ID.
    
    This function queries the database for a product with the given ID and returns its details.
    
    Args:
        product_id (int): The ID of the product to retrieve.
    
    Returns:
        tuple: A tuple containing:
            - A JSON object with the product's details.
            - HTTP status code 200.
    
    Raises:
        HTTPException: 404 Not Found if the product does not exist.
    """
    #product = Product.query.get_or_404(product_id)
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({'msg': 'Product not found'}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock
    }), 200

@products_bp.route('/products', methods=['POST'])
@admin_required
def add_product():
    """
    Add a new product to the database.
    
    This function creates a new product with the provided details and adds it to the database.
    It requires admin privileges.
    
    Returns:
        tuple: A tuple containing:
            - A JSON object with a success message and the new product's ID.
            - HTTP status code 201 if successful, 400 for bad request, or 500 for server error.
    
    Raises:
        HTTPException: 400 Bad Request if required fields are missing.
        HTTPException: 500 Internal Server Error if there's a database error.
    """
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"msg": "Name and price are required fields"}), 400

    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data.get('stock', 0)
    )
    try:
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "msg": "An error occurred while adding the product",
            "error": str(e)
        }), 500
    return jsonify({
        "msg": "Product added",
        "product_id": product.id
    }), 201

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required
def edit_product(product_id):
    """
    Edit an existing product.
    
    This function updates the details of an existing product with the given ID.
    It requires admin privileges.
    
    Args:
        product_id (int): The ID of the product to edit.
    
    Returns:
        tuple: A tuple containing:
            - A JSON object with a success message and the updated product's ID.
            - HTTP status code 200 if successful, 400 for bad request, or 500 for server error.
    
    Raises:
        HTTPException: 404 Not Found if the product does not exist.
        HTTPException: 400 Bad Request if no data is provided.
        HTTPException: 500 Internal Server Error if there's a database error.
    """
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided"}), 400

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "msg": "An error occurred while updating the product",
            "error": str(e)
        }), 500
    return jsonify({
        "msg": "Product updated",
        "product_id": product.id
    }), 200

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """
    Delete a product from the database.
    
    This function removes a product with the given ID from the database.
    It requires admin privileges.
    
    Args:
        product_id (int): The ID of the product to delete.
    
    Returns:
        tuple: A tuple containing:
            - A JSON object with a success message.
            - HTTP status code 200 if successful, or 500 for server error.
    
    Raises:
        HTTPException: 404 Not Found if the product does not exist.
        HTTPException: 500 Internal Server Error if there's a database error.
    """
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "msg": "An error occurred while deleting the product",
            "error": str(e)
        }), 500
    return jsonify({"msg": "Product deleted"}), 200
