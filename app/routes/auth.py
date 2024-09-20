"""
auth.py:

Authentication Blueprint for E-commerce Backend

This module defines the authentication routes for user registration and login.
It uses Flask-JWT-Extended for token-based authentication.

Routes:
    /register (POST): Register a new user
    /login (POST): Authenticate a user and return an access token

Functions:
    register(): Handle user registration
    login(): Handle user login and token generation

Dependencies:
    Flask: Web framework for building the API
    Flask-JWT-Extended: Handles JWT token generation and management
    SQLAlchemy: ORM for database interactions (via app.models)

Models:
    User: Represents the user entity in the database

Usage:
    This blueprint should be registered with the main Flask application.
    It interacts with the User model to create new users and verify credentials.

Note:
    Ensure that Flask-JWT-Extended is properly configured in the main application.
    Passwords are hashed before storing in the database for security.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import db, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    This endpoint allows a new user to register by providing a username, email,
    and password. It checks for the existence of the username and email in the
    database to ensure they are unique. If the registration is successful,
    the user is added to the database.

    Request:
        POST /register
        JSON body should contain:
            - username (str): The desired username for the new user.
            - email (str): The email address of the new user.
            - password (str): The password for the new user account.

    Responses:
        - 201: User registered successfully.
        - 400: Username or email already exists.
    """
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "Username already exists"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "Email already exists"}), 400
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Log in an existing user.

    This endpoint allows a registered user to log in by providing their username
    and password. If the credentials are valid, an access token is generated
    and returned. Otherwise, an error message is returned.

    Request:
        POST /login
        JSON body should contain:
            - username (str): The username of the user attempting to log in.
            - password (str): The password for the user's account.

    Responses:
        - 200: Access token generated successfully.
        - 401: Invalid credentials provided.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401
