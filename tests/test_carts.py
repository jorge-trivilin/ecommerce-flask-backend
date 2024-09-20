"""
Unit tests for cart functionality in a Flask application.

This module tests cart operations, including adding/removing products and handling empty carts.

Fixtures:
- `app`: Sets up a Flask app with a test database, creating and dropping tables as needed.
- `client`: Provides a test client for making requests.
- `auth_headers`: Creates a test user and provides authorization headers.
- `sample_product`: Adds a sample product to the database for testing.

Test Cases:
- `test_view_empty_cart`: Ensures an empty cart returns an empty list.
- `test_add_to_cart`: Verifies adding a product to the cart and its quantity.
- `test_remove_from_cart`: Tests removing a product and checks for an empty cart.
- `test_remove_nonexistent_item`: Checks 404 error for removing a non-existent item.
- `test_add_existing_product`: Validates updating quantity when adding an existing product.

Logging:
- Uses the logging library for debug-level logs on database operations, routes, and test actions.

Dependencies:
- `pytest`: Testing framework.
- `flask`: Web framework.
- `app`: Application components (e.g., `create_app`, `db`, `User`, `Product`).
- `config`: Test environment settings.

Usage:
- Run with `pytest` to verify cart functionality.
"""
# pylint: disable=unused-argument
# pylint: disable=duplicate-code
import logging
import pytest
from flask import json
from app import create_app
from app.extensions import db
from app.models import User, Product
from config import TestConfig

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.fixture
def app():
    """
    Fixture that creates and configures a new Flask application instance for testing.

    It sets up the application context, creates the database tables, and logs
    the registered routes. After yielding the application, it removes the database
    session and drops all tables to clean up.

    Returns:
        Flask app: The configured Flask application instance.
    """
    app = create_app(TestConfig)
    with app.app_context():
        logger.info("Creating database tables")
        db.create_all()
        logger.info("Database tables created")

        # Print all registered routes
        for rule in app.url_map.iter_rules():
            logger.debug(f"Registered route: {rule}")

        yield app
        logger.info("Removing database session")
        db.session.remove()
        logger.info("Dropping all tables")
        db.drop_all()
        logger.info("All tables dropped")


@pytest.fixture
def client(app):
    """
    Fixture that provides a test client for the Flask application.

    This client is used to make requests to the application during tests.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        FlaskClient: The test client for the Flask application.
    """
    return app.test_client()


@pytest.fixture
def auth_headers(app, client):
    """
    Fixture that creates a test user, logs them in, and provides the authorization headers.

    It creates a user, sets their password, and logs in to obtain an authentication token.
    The token is used for making authorized requests in the tests.

    Args:
        app (Flask): The Flask application instance.
        client (FlaskClient): The test client for the Flask application.

    Returns:
        dict: Authorization headers with the Bearer token.
    """
    with app.app_context():
        logger.info("Creating test user")
        user = User(username="testuser", email="test@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        logger.info("Test user created")

    # Log in and get the token
    response = client.post(
        "/auth/login", json={"username": "testuser", "password": "password"}
    )
    data = json.loads(response.data)
    token = data.get("access_token")

    if not token:
        pytest.fail(f"Failed to get token. Response: {data}")

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_product(app):
    """
    Fixture to create a sample product for testing.

    This fixture creates a product instance, adds it to the database, and returns it.
    The product can be used in tests to verify cart operations.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        Product: The created product instance.
    """
    with app.app_context():
        product = Product(name="Sample Product", price=10.0, stock=100)
        db.session.add(product)
        db.session.commit()

        # Access the product ID to prevent it from being loaded later (e.g.,
        # lazy load)
        product_id = product.id  # pylint: disable=unused-argument
        return product


def test_view_empty_cart(client, auth_headers):
    """
    Test the endpoint for viewing an empty cart.

    Makes a GET request to the cart endpoint and verifies that the cart is empty.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_headers (dict): Authorization headers with the Bearer token.
    """
    response = client.get("/cart", headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["cart"] == []


def test_add_to_cart(client, auth_headers, sample_product):
    """
    Test adding a product to the cart.

    Makes a POST request to add a product to the cart and verifies that the product
    has been added with the correct quantity. Then, it checks if the cart contains
    the product with the expected quantity.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_headers (dict): Authorization headers with the Bearer token.
        sample_product (Product): The sample product instance to add to the cart.
    """
    response = client.post(
        "/cart",
        json={"product_id": sample_product.id, "quantity": 2},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert json.loads(response.data)["msg"] == "Product added to cart"

    # Check if product was added to cart
    response = client.get("/cart", headers=auth_headers)
    data = json.loads(response.data)
    assert len(data["cart"]) == 1
    assert data["cart"][0]["product_id"] == sample_product.id
    assert data["cart"][0]["quantity"] == 2


def test_remove_from_cart(client, auth_headers, sample_product):
    """
    Test removing a product from the cart.

    Adds a product to the cart and then removes it. Verifies that the product
    has been successfully removed and the cart is empty afterwards.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_headers (dict): Authorization headers with the Bearer token.
        sample_product (Product): The sample product instance to remove from the cart.
    """
    # Adding product to cart
    client.post(
        "/cart",
        json={"product_id": sample_product.id, "quantity": 1},
        headers=auth_headers,
    )

    # Removing product from cart
    response = client.delete(
        f"/cart/{sample_product.id}",
        headers=auth_headers)
    assert response.status_code == 200
    assert json.loads(response.data)[
        "msg"] == "Item successfully removed from cart"

    # Check if cart is empty
    response = client.get("/cart", headers=auth_headers)
    data = json.loads(response.data)
    assert data["cart"] == []


def test_remove_nonexistent_item(client, auth_headers):
    """
    Test removing a non-existent item from the cart.

    Attempts to remove an item that does not exist in the cart and verifies
    that a 404 Not Found error is returned with an appropriate message.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_headers (dict): Authorization headers with the Bearer token.
    """
    response = client.delete("/cart/999", headers=auth_headers)
    assert response.status_code == 404
    assert json.loads(response.data)["msg"] == "Cart not found"


def test_add_existing_product(client, auth_headers, sample_product):
    """
    Test adding an existing product to the cart and updating the quantity.

    Adds a product to the cart for the first time, then adds the same product again
    with a different quantity. Verifies that the quantity is updated correctly in the cart.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_headers (dict): Authorization headers with the Bearer token.
        sample_product (Product): The sample product instance to add to the cart.
    """
    # Adding product for the first time
    client.post(
        "/cart",
        json={"product_id": sample_product.id, "quantity": 1},
        headers=auth_headers,
    )

    # Adding the same product again
    response = client.post(
        "/cart",
        json={"product_id": sample_product.id, "quantity": 2},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert json.loads(response.data)["msg"] == "Product added to cart"

    # Check if quantity was updated
    response = client.get("/cart", headers=auth_headers)
    data = json.loads(response.data)
    assert len(data["cart"]) == 1
    assert data["cart"][0]["product_id"] == sample_product.id
    assert data["cart"][0]["quantity"] == 3


def test_clear_cart(client, auth_headers, sample_product):
    """
    Test clearing the cart.

    This test ensures that the entire cart is cleared
    when calling the clear_cart endpoint.
    It first adds a product to the cart, then calls the clear
    endpoint and verifies that the cart is empty.
    """
    # Add a product to the cart
    client.post(
        "/cart",
        json={"product_id": sample_product.id, "quantity": 1},
        headers=auth_headers,
    )

    # Verify the cart is not empty
    response = client.get("/cart", headers=auth_headers)
    data = json.loads(response.data)
    assert len(data["cart"]) == 1

    # Clear the cart
    response = client.delete("/cart/clear", headers=auth_headers)
    assert response.status_code == 200
    assert json.loads(response.data)["msg"] == "Cart cleared"

    # Verify the cart is empty
    response = client.get("/cart", headers=auth_headers)
    data = json.loads(response.data)
    assert data["cart"] == []
