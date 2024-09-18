"""
Unit tests for order-related functionalities in the Flask application.

This module provides test cases for the ordering process, including placing orders,
retrieving order history, and fetching details for specific orders. It ensures that
the order management system functions correctly under various scenarios.

Fixtures:
- `app`: Creates and configures a Flask application instance with a test database.
  - **Setup**: Initializes database tables, logs routes, and sets up the application context.
  - **Teardown**: Cleans up by removing the database session and dropping all tables.

- `client`: Provides a test client for making HTTP requests to the application.

- `auth_headers`: Creates a test user, logs in, and returns the authorization headers
  with a Bearer token for authenticated requests.

- `sample_user`: Creates a sample user with a predefined username and email
  if it does not already exist.

- `sample_product`: Creates a sample product with predefined attributes.

- `sample_cart`: Creates a sample cart associated with the sample user and adds
  an item to it.

Test Cases:
- `test_place_order_with_empty_cart`: Tests the behavior when attempting
to place an order
  with an empty cart.
  - **Assertions**: Ensures the response status code is 400,
  and the message indicates the cart is empty.

- `test_place_order_success`: Verifies that an order can be placed successfully when
  there are items in the cart.
  - **Assertions**: Checks the status code, response message, presence of an order ID,
    and ensures the cart is cleared after the order is placed.

- `test_get_order_history`: Tests retrieving the order history for a user.
  - **Assertions**: Ensures the response status code is 200, verifies the order history
    contains the placed order, and checks the count of items in the order.

- `test_get_order_details`: Verifies that details for a specific order can be retrieved.
  - **Assertions**: Checks the status code, verifies the presence of order details,
    and ensures that the order ID and items are correctly returned.

- `test_get_nonexistent_order_details`: Tests the response when trying to retrieve
  details for a non-existent order.
  - **Assertions**: Ensures the response status code is 404 and the message indicates
    the order was not found.

Logging:
- The module uses the logging library for debugging, including creating database tables,
  logging routes, and actions during test setup.

Dependencies:
- `pytest`: Framework used for writing and running the tests.
- `flask`: Web framework for the application.
- `app`: Application components including `create_app`, `db`, and model classes (`User`,
  `Cart`, `CartItem`, `Product`, `Order`, `OrderItem`).
- `config`: Configuration settings for the test environment.

Usage:
- Run the tests using `pytest` to verify the correctness of order-related functionalities.
  Example command: `pytest test_orders.py`
"""
# pylint: disable=duplicate-code
import logging
import pytest
from flask import json
from app import create_app
from app.extensions import db
from app.models import User, Cart, CartItem, Product
from config import TestConfig

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.fixture
def app():
    """
    Fixture for creating and configuring the Flask application.

    Sets up the application context and creates the database tables before yielding
    the app instance. After tests complete, it removes the database session and
    drops all tables to clean up.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = create_app(TestConfig)
    with app.app_context():
        logger.debug("Creating database tables")
        db.create_all()
        logger.debug("Database tables created")

        # Print all registered routes
        for rule in app.url_map.iter_rules():
            logger.debug(f"Registered route: {rule}")

        yield app
        logger.debug("Removing database session")
        db.session.remove()
        logger.debug("Dropping all tables")
        db.drop_all()
        logger.debug("All tables dropped")


@pytest.fixture
def client(app):
    """
    Fixture for creating a test client for the application.

    Provides a test client that can be used to make HTTP requests to the application
    during tests.

    Returns:
        FlaskClient: The test client instance.
    """
    return app.test_client()


@pytest.fixture
def auth_headers(app, client):
    """
    Fixture for generating authentication headers for requests.

    Creates a test user, logs in to obtain a token, and returns the headers
    required for authenticated requests.

    Returns:
        dict: Headers including the Bearer token for authentication.
    """
    with app.app_context():
        logger.debug("Creating test user")
        user = User(username="testuser", email="test@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        logger.debug("Test user created")

    # Log in and get the token
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "password"})
    data = json.loads(response.data)
    token = data.get("access_token")

    if not token:
        pytest.fail(f"Failed to get token. Response: {data}")

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_user(app):
    """
    Fixture to create a sample user.

    Creates a user with predefined username and email if it does not already exist
    in the database.

    Returns:
        User: The created or existing sample user.
    """
    with app.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        if not user:
            user = User(username="testuser", email="test@example.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()
        return user


@pytest.fixture
def sample_product(app):
    """
    Fixture to create a sample product.

    Adds a sample product with predefined attributes to the database.

    Returns:
        Product: The created sample product.
    """
    with app.app_context():
        product = Product(name="Sample Product", price=10.0, stock=100)
        db.session.add(product)
        db.session.commit()
        return product


@pytest.fixture
def sample_cart(app, sample_user, sample_product):
    """
    Fixture to create a sample cart with an item.

    Creates a cart associated with the sample user and adds a sample product
    to it with a specified quantity.

    Returns:
        Cart: The created sample cart with an item.
    """
    with app.app_context():
        cart = Cart(user_id=sample_user.id)
        cart_item = CartItem(cart=cart, product=sample_product, quantity=2)
        db.session.add(cart)
        db.session.add(cart_item)
        db.session.commit()
        return cart


def test_place_order_with_empty_cart(client, auth_headers, sample_user):  # pylint: disable=unused-argument
    """
    Test placing an order with an empty cart.

    Attempts to place an order when the cart is empty and verifies that the
    response indicates the cart is empty.

    Parameters:
        client (FlaskClient): The test client for making HTTP requests.
        auth_headers (dict): Headers including the Bearer token for authentication.
        sample_user (User): The sample user for the test.
    """
    response = client.post("/orders", headers=auth_headers)
    assert response.status_code == 400
    assert json.loads(response.data)["msg"] == "Cart is empty"


def test_place_order_success(client, auth_headers, sample_cart):  # pylint: disable=unused-argument
    """
    Test placing an order successfully with items in the cart.

    Places an order with items in the cart and verifies that the order is placed
    successfully. Also checks that the cart is cleared after the order.

    Parameters:
        client (FlaskClient): The test client for making HTTP requests.
        auth_headers (dict): Headers including the Bearer token for authentication.
        sample_cart (Cart): The sample cart with items for the test.
    """
    response = client.post("/orders", headers=auth_headers)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["msg"] == "Order placed successfully"
    assert "order_id" in data

    # Verify that the cart is cleared after placing the order
    cart_response = client.get("/cart", headers=auth_headers)
    cart_data = json.loads(cart_response.data)
    assert cart_data["cart"] == []


def test_get_order_history(client, auth_headers, sample_cart):  # pylint: disable=unused-argument
    """
    Test retrieving the order history of a user.

    Places an order and then retrieves the order history to verify that the order
    appears in the history with correct details.

    Parameters:
        client (FlaskClient): The test client for making HTTP requests.
        auth_headers (dict): Headers including the Bearer token for authentication.
        sample_cart (Cart): The sample cart used to place an order for the test.
    """
    # Place an order first
    client.post("/orders", headers=auth_headers)

    # Fetch order history
    response = client.get("/orders/history", headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["orders"]) == 1
    assert "id" in data["orders"][0]
    assert data["orders"][0]["items_count"] > 0


def test_get_order_details(client, auth_headers, sample_cart):  # pylint: disable=unused-argument
    """
    Test retrieving the details of a specific order.

    Places an order and then retrieves the details of that specific order to ensure
    that the order details are correctly returned.

    Parameters:
        client (FlaskClient): The test client for making HTTP requests.
        auth_headers (dict): Headers including the Bearer token for authentication.
        sample_cart (Cart): The sample cart used to place an order for the test.
    """
    # Place an order first
    response = client.post("/orders", headers=auth_headers)
    order_id = json.loads(response.data)["order_id"]

    # Get the details of the placed order
    response = client.get(f"/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "order" in data
    assert data["order"]["id"] == order_id
    assert len(data["order"]["items"]) > 0


def test_get_nonexistent_order_details(client, auth_headers):
    """
    Test retrieving details for a non-existent order.

    Attempts to retrieve details for an order that does not exist and verifies
    that the response indicates the order was not found.

    Parameters:
        client (FlaskClient): The test client for making HTTP requests.
        auth_headers (dict): Headers including the Bearer token for authentication.
    """
    response = client.get("/orders/999", headers=auth_headers)
    assert response.status_code == 404
    assert json.loads(response.data)["msg"] == "Pedido não encontrado"
