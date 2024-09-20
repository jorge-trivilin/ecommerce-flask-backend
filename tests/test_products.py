"""
Test suite for product-related API endpoints.

This module contains unit tests for the product management functionality of
the e-commerce backend. It tests various operations, including retrieving
products, adding products, updating products, and deleting products.

Each test is performed using a test client and an in-memory SQLite database.
"""

import pytest
from flask_jwt_extended import create_access_token, JWTManager
from werkzeug.security import generate_password_hash
from flask import Flask
from app.models import db, User, Product
from app.routes.products import products_bp


@pytest.fixture(scope="function")
def fixture_app():
    """
    Creates a Flask application configured for testing.

    This fixture sets up a Flask application with testing configurations, an
    in-memory SQLite database, and initializes the necessary extensions and
    routes. It also creates an admin and a regular user in the database for
    testing purposes.

    Yields:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(products_bp)

    with app.app_context():
        db.create_all()

        # Create an admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            is_admin=True,
            password_hash=generate_password_hash("adminpass"),
        )
        db.session.add(admin_user)

        # Create a regular user
        regular_user = User(
            username="user",
            email="user@example.com",
            is_admin=False,
            password_hash=generate_password_hash("userpass"),
        )
        db.session.add(regular_user)

        db.session.commit()

    yield app

    # Teardown
    with app.app_context():
        db.drop_all()


@pytest.fixture
def fixture_client(fixture_app):
    """
    Provides a test client for the Flask application.

    This fixture returns a test client that can be used to make HTTP requests
    to the Flask application during testing.

    Parameters:
        fixture_app (Flask): The Flask application instance.

    Returns:
        FlaskClient: The test client instance.
    """
    return fixture_app.test_client()


@pytest.fixture
def fixture_admin_jwt_token(fixture_app):
    """
    Generates a JWT token for the admin user.

    This fixture creates a JWT token for the admin user, which can be used to
    authenticate admin requests during testing.

    Parameters:
        fixture_app (Flask): The Flask application instance.

    Returns:
        str: JWT token for the admin user.
    """
    with fixture_app.app_context():
        admin = User.query.filter_by(username="admin").first()
        return create_access_token(identity=admin.id)


@pytest.fixture
def fixture_user_jwt_token(fixture_app):
    """
    Generates a JWT token for the regular user.

    This fixture creates a JWT token for the regular user, which can be used
    to authenticate regular user requests during testing.

    Parameters:
        fixture_app (Flask): The Flask application instance.

    Returns:
        str: JWT token for the regular user.
    """
    with fixture_app.app_context():
        user = User.query.filter_by(username="user").first()
        return create_access_token(identity=user.id)


@pytest.fixture
def fixture_sample_product(fixture_app):
    """
    Creates a sample product in the database and returns its ID.

    This fixture adds a sample product to the database, which can be used in
    tests that require a product to be present.

    Parameters:
        fixture_app (Flask): The Flask application instance.

    Returns:
        int: The ID of the created sample product.
    """
    with fixture_app.app_context():
        product = Product(
            name="Sample Product",
            description="This is a sample product.",
            price=19.99,
            stock=100,
        )
        db.session.add(product)
        db.session.commit()

        assert Product.query.count() == 1

        return product.id


def test_get_all_products(fixture_client, fixture_app, fixture_sample_product):
    """
    Tests retrieving all products.

    This test checks that all products are retrieved correctly from the API.
    It verifies that the sample product added in the fixture is present in
    the response.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_app (Flask): The Flask application instance.
        fixture_sample_product (int): The ID of the sample product.
    """
    with fixture_app.app_context():
        assert Product.query.count() == 1
        db_product = Product.query.get(fixture_sample_product)
        assert db_product is not None
        assert db_product.id == fixture_sample_product
        assert db_product.name == "Sample Product"

    response = fixture_client.get("/products")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Sample Product"
    assert data[0]["id"] == fixture_sample_product


def test_get_single_product(fixture_client, fixture_sample_product):
    """
    Tests retrieving a single product by ID.

    This test verifies that details of a single product can be retrieved by
    its ID. It checks that the product's attributes match the expected values.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_sample_product (int): The ID of the sample product.
    """
    response = fixture_client.get(f"/products/{fixture_sample_product}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Sample Product"
    assert data["description"] == "This is a sample product."
    assert data["price"] == 19.99
    assert data["stock"] == 100


def test_get_nonexistent_product(fixture_client):
    """
    Tests retrieving a product that doesn't exist.

    This test checks that the API returns a 404 error when attempting to
    retrieve a product with an ID that does not exist in the database.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
    """
    response = fixture_client.get("/products/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["msg"] == "Product not found"


def test_add_product_as_admin(fixture_client, fixture_admin_jwt_token):
    """
    Tests adding a new product as an admin.

    This test verifies that an admin user can add a new product to the database
    and that the response confirms the addition. It also checks that the product
    is correctly added by querying the database.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_admin_jwt_token (str): JWT token for the admin user.
    """
    new_product = {
        "name": "New Product",
        "description": "A brand new product.",
        "price": 29.99,
        "stock": 50,
    }
    response = fixture_client.post(
        "/products",
        json=new_product,
        headers={"Authorization": f"Bearer {fixture_admin_jwt_token}"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Product added"
    assert "product_id" in data

    # Verify that the product was added
    with fixture_client.application.app_context():
        product = Product.query.get(data["product_id"])
        assert product is not None
        assert product.name == "New Product"


def test_add_product_as_non_admin(fixture_client, fixture_user_jwt_token):
    """
    Tests adding a new product as a non-admin user.

    This test checks that a regular user (non-admin) cannot add a new product
    and that the API returns a 403 error indicating that admin privileges are
    required.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_user_jwt_token (str): JWT token for the regular user.
    """
    new_product = {
        "name": "Unauthorized Product",
        "description": "Should not be added.",
        "price": 9.99,
        "stock": 10,
    }
    response = fixture_client.post(
        "/products",
        json=new_product,
        headers={"Authorization": f"Bearer {fixture_user_jwt_token}"},
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["msg"] == "Admin privilege required"


def test_add_product_missing_fields(fixture_client, fixture_admin_jwt_token):
    """
    Tests adding a new product with missing required fields.

    This test checks that the API returns a 400 error when attempting to add
    a product with missing required fields (e.g., name and price).

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_admin_jwt_token (str): JWT token for the admin user.
    """
    incomplete_product = {"description": "Missing name and price."}
    response = fixture_client.post(
        "/products",
        json=incomplete_product,
        headers={"Authorization": f"Bearer {fixture_admin_jwt_token}"},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["msg"] == "Name and price are required fields"


def test_edit_product_as_admin(
    fixture_client, fixture_admin_jwt_token, fixture_sample_product
):
    """
    Tests editing an existing product as an admin.

    This test verifies that an admin user can update the details of an existing
    product and that the changes are correctly applied. It checks that the
    response confirms the update and verifies the changes in the database.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_admin_jwt_token (str): JWT token for the admin user.
        fixture_sample_product (int): The ID of the sample product.
    """
    updated_product = {
        "name": "Updated Product",
        "description": "Updated description.",
        "price": 39.99,
        "stock": 75,
    }
    response = fixture_client.put(
        f"/products/{fixture_sample_product}",
        json=updated_product,
        headers={"Authorization": f"Bearer {fixture_admin_jwt_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Product updated"

    # Verify the product was updated
    with fixture_client.application.app_context():
        product = Product.query.get(fixture_sample_product)
        assert product is not None
        assert product.name == "Updated Product"
        assert product.description == "Updated description."
        assert product.price == 39.99
        assert product.stock == 75


def test_edit_product_as_non_admin(
    fixture_client, fixture_user_jwt_token, fixture_sample_product
):
    """
    Tests editing an existing product as a non-admin user.

    This test checks that a regular user (non-admin) cannot edit an existing
    product and that the API returns a 403 error indicating that admin privileges
    are required.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_user_jwt_token (str): JWT token for the regular user.
        fixture_sample_product (int): The ID of the sample product.
    """
    updated_product = {
        "name": "Unauthorized Update",
        "description": "Should not be allowed.",
        "price": 49.99,
        "stock": 60,
    }
    response = fixture_client.put(
        f"/products/{fixture_sample_product}",
        json=updated_product,
        headers={"Authorization": f"Bearer {fixture_user_jwt_token}"},
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["msg"] == "Admin privilege required"


def test_delete_product_as_admin(
    fixture_client, fixture_admin_jwt_token, fixture_sample_product
):
    """
    Tests deleting a product as an admin.

    This test verifies that an admin user can delete a product and that the
    product is no longer present in the database after deletion. It checks that
    the response confirms the deletion.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_admin_jwt_token (str): JWT token for the admin user.
        fixture_sample_product (int): The ID of the sample product.
    """
    response = fixture_client.delete(
        f"/products/{fixture_sample_product}",
        headers={"Authorization": f"Bearer {fixture_admin_jwt_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Product deleted"

    # Verify the product was deleted
    with fixture_client.application.app_context():
        product = Product.query.get(fixture_sample_product)
        assert product is None


def test_delete_product_as_non_admin(
    fixture_client, fixture_user_jwt_token, fixture_sample_product
):
    """
    Tests deleting a product as a non-admin user.

    This test checks that a regular user (non-admin) cannot delete a product
    and that the API returns a 403 error indicating that admin privileges are
    required.

    Parameters:
        fixture_client (FlaskClient): The test client for making HTTP requests.
        fixture_user_jwt_token (str): JWT token for the regular user.
        fixture_sample_product (int): The ID of the sample product.
    """
    response = fixture_client.delete(
        f"/products/{fixture_sample_product}",
        headers={"Authorization": f"Bearer {fixture_user_jwt_token}"},
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["msg"] == "Admin privilege required"
