"""
extensions.py

This module initializes and configures extensions for the Flask application.
It creates instances of commonly used extensions, which can be imported 
and used throughout the application.

Extensions:
- db: An instance of SQLAlchemy used for database interactions and ORM 
  (Object-Relational Mapping).
- jwt: An instance of JWTManager used for managing JSON Web Tokens for 
  authentication and authorization.

Usage:
To use these extensions in other parts of the application, import them as follows:

    from app.extensions import db, jwt

This allows for seamless integration of database operations and JWT handling 
within the Flask app.

Example:
    from app.extensions import db

    class User(db.Model):
        # Define user model here

"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()
