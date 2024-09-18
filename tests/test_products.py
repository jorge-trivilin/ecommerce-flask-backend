"""
Test suite for product-related API endpoints.

This module contains unit tests for the product management functionality of
the e-commerce backend. It tests various operations, including retrieving
products, adding products, updating products, and deleting products.

Each test is performed using a test client e um banco de dados SQLite em memória.
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
    Creates a Flask application configured para testing.
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
    """
    return fixture_app.test_client()


@pytest.fixture
def fixture_admin_jwt_token(fixture_app):
    """
    Generates a JWT token para o usuário admin.
    """
    with fixture_app.app_context():
        admin = User.query.filter_by(username="admin").first()
        return create_access_token(identity=admin.id)


@pytest.fixture
def fixture_user_jwt_token(fixture_app):
    """
    Generates a JWT token para o usuário regular.
    """
    with fixture_app.app_context():
        user = User.query.filter_by(username="user").first()
        return create_access_token(identity=user.id)


@pytest.fixture
def fixture_sample_product(fixture_app):
    """
    Creates a sample product in the database and returns its ID.
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
    """
    response = fixture_client.get("/products/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["msg"] == "Product not found"


def test_add_product_as_admin(fixture_client, fixture_admin_jwt_token):
    """
    Tests adding a new product as an admin.
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
    """
    updated_data = {"name": "Updated Product", "price": 24.99, "stock": 80}
    response = fixture_client.put(
        f"/products/{fixture_sample_product}",
        json=updated_data,
        headers={"Authorization": f"Bearer {fixture_admin_jwt_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Product updated"
    assert data["product_id"] == fixture_sample_product

    # Verify that the product was updated
    with fixture_client.application.app_context():
        product = Product.query.get(fixture_sample_product)
        assert product.name == "Updated Product"
        assert product.price == 24.99
        assert product.stock == 80


def test_edit_product_as_non_admin(
    fixture_client, fixture_user_jwt_token, fixture_sample_product
):
    """
    Tests editing a product as a non-admin user.
    """
    updated_data = {"name": "Hacked Product", "price": 0.99}
    response = fixture_client.put(
        f"/products/{fixture_sample_product}",
        json=updated_data,
        headers={"Authorization": f"Bearer {fixture_user_jwt_token}"},
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["msg"] == "Admin privilege required"


def test_edit_product_no_data(
    fixture_client, fixture_admin_jwt_token, fixture_sample_product
):
    """
    Tests editing a product without providing any data.
    """
    response = fixture_client.put(
        f"/products/{fixture_sample_product}",
        json={},
        headers={"Authorization": f"Bearer {fixture_admin_jwt_token}"},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["msg"] == "No data provided"


def test_delete_product_as_admin(
    fixture_client, fixture_admin_jwt_token, fixture_sample_product
):
    """
    Tests deleting a product as an admin.
    """
    response = fixture_client.delete(
        f"/products/{fixture_sample_product}",
        headers={"Authorization": f"Bearer {fixture_admin_jwt_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Product deleted"

    # Verify that the product was deleted
    with fixture_client.application.app_context():
        product = Product.query.get(fixture_sample_product)
        assert product is None


def test_delete_product_as_non_admin(
    fixture_client, fixture_user_jwt_token, fixture_sample_product
):
    """
    Tests deleting a product as a non-admin user.
    """
    response = fixture_client.delete(
        f"/products/{fixture_sample_product}",
        headers={"Authorization": f"Bearer {fixture_user_jwt_token}"},
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["msg"] == "Admin privilege required"


def test_delete_nonexistent_product(fixture_client, fixture_admin_jwt_token):
    """
    Tests deleting a product that doesn't exist.
    """
    response = fixture_client.delete(
        "/products/999",
        headers={
            "Authorization": f"Bearer {fixture_admin_jwt_token}"})
    assert response.status_code == 404
    data = response.get_json()
    assert data["msg"] == "Product not found"
