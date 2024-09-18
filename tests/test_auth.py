"""
Unit tests for authentication features in the Flask application.

This module includes test cases for user registration and login processes, ensuring that 
authentication endpoints work as expected across various scenarios, both successful and failed.

Fixtures:
- `app`: Sets up and tears down the Flask application with a test database.
- `session`: Provides a fresh SQLAlchemy database session for each test.
- `client`: A test client for making HTTP requests.
- `new_user_data`: Sample data for registering a new user.
- `sample_user`: A sample user for authentication tests.

Test Cases:
- `test_register_user`: Verifies successful user registration and database update.
- `test_register_existing_username`: Checks response for registration with an existing username.
- `test_register_existing_email`: Validates response for registration with an existing email.
- `test_login_success`: Confirms successful login with valid credentials and access token.
- `test_login_invalid_credentials`: Tests login failure with invalid credentials.

Logging:
- Utilizes the `logging` library for debugging database operations and test actions.

Dependencies:
- `pytest`: Testing framework.
- `flask`: Web framework.
- `app`: Application components (`create_app`, `User`, `db`).
- `config`: Test configuration settings.

Usage:
- Run tests with `pytest` to verify authentication functionality.
  Example command: `pytest test_auth.py`
"""

import logging
import pytest
from flask import json
from app import create_app
from app.models import User
from app.extensions import db
from config import TestConfig

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def app():
    """
    Fixture for creating and configuring the Flask application.

    Sets up the application context and creates the database tables 
    before yielding the app instance. After tests complete, it removes 
    the database session and drops all tables to clean up.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = create_app(TestConfig)
    with app.app_context():
        logger.debug("Creating database tables")
        db.create_all()
        logger.debug("Database tables created")
        yield app
        logger.debug("Removing database session")
        db.session.remove()
        logger.debug("Dropping all tables")
        db.drop_all()
        logger.debug("All tables dropped")

@pytest.fixture(scope="function")
def session(app):
    """
    Fixture for creating a new database session for each test.

    This fixture sets up a new database schema for each test function,
    ensuring that tests do not interfere with each other. After the test,
    it removes the session and drops all tables.

    Returns:
        Session: The SQLAlchemy session instance.
    """
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Fixture for creating a test client for the application.

    This fixture provides a test client that can be used to make requests 
    to the application during tests.

    Returns:
        FlaskClient: The test client instance.
    """
    return app.test_client()

@pytest.fixture
def new_user_data():
    """Fixture for generating new user registration data."""
    return {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password",
    }

@pytest.fixture
def sample_user(session):
    """Fixture to create a sample user."""
    user = User.query.filter_by(email="test@example.com").first()
    if not user:
        user = User(username="testuser", email="test@example.com")
        user.set_password("password")
        session.add(user)
        session.commit()
    return user

def test_register_user(client, new_user_data):
    """Test registering a new user successfully."""
    response = client.post("/api/auth/register", json=new_user_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["msg"] == "User registered successfully"
    user = User.query.filter_by(email=new_user_data["email"]).first()
    assert user is not None
    assert user.username == new_user_data["username"]

def test_register_existing_username(client, sample_user):
    """Test registering a user with an existing username."""
    existing_user_data = {
        "username": sample_user.username,
        "email": "anotheremail@example.com",
        "password": "password",
    }
    response = client.post("/api/auth/register", json=existing_user_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["msg"] == "Username already exists"

def test_register_existing_email(client, sample_user):
    """Test registering a user with an existing email."""
    existing_email_data = {
        "username": "anotheruser",
        "email": sample_user.email,
        "password": "password",
    }
    response = client.post("/api/auth/register", json=existing_email_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["msg"] == "Email already exists"

def test_login_success(client, sample_user):
    """Test logging in with valid credentials."""
    login_data = {"username": sample_user.username, "password": "password"}
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data

def test_login_invalid_credentials(client):
    """Test logging in with invalid credentials."""
    invalid_login_data = {"username": "wronguser", "password": "wrongpassword"}
    response = client.post("/api/auth/login", json=invalid_login_data)
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data["msg"] == "Invalid credentials"