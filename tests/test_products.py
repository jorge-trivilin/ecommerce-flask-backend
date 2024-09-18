# tests/test_products.py

import pytest
from flask_jwt_extended import create_access_token, JWTManager
from app.models import db, User, Product
from app.routes.products import products_bp
from werkzeug.security import generate_password_hash
from flask import Flask

@pytest.fixture(scope='function')
def test_app():
    """
    Creates a Flask application configured for testing.
    """
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)  # Initialize JWTManager
    app.register_blueprint(products_bp)

    with app.app_context():
        db.create_all()

        # Create an admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            is_admin=True,
            password_hash=generate_password_hash('adminpass')
        )
        db.session.add(admin_user)

        # Create a regular user
        regular_user = User(
            username='user',
            email='user@example.com',
            is_admin=False,
            password_hash=generate_password_hash('userpass')
        )
        db.session.add(regular_user)

        db.session.commit()

    yield app

    # Teardown
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(test_app):
    """
    Provides a test client for the Flask application.
    """
    return test_app.test_client()

@pytest.fixture
def admin_token(test_app):
    """
    Generates a JWT token for the admin user.
    """
    with test_app.app_context():
        admin = User.query.filter_by(username='admin').first()
        return create_access_token(identity=admin.id)

@pytest.fixture
def user_token(test_app):
    """
    Generates a JWT token for the regular user.
    """
    with test_app.app_context():
        user = User.query.filter_by(username='user').first()
        return create_access_token(identity=user.id)

@pytest.fixture
def sample_product(test_app):
    """
    Creates a sample product in the database.
    """
    with test_app.app_context():
        product = Product(
            name='Sample Product',
            description='This is a sample product.',
            price=19.99,
            stock=100
        )
        db.session.add(product)
        db.session.commit()
        return product.id

def test_get_all_products(client, sample_product):
    """
    Tests retrieving all products.
    """
    response = client.get('/products')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'Sample Product'

def test_get_single_product(client, test_app, sample_product):
    """
    Tests retrieving a single product by ID.
    """
    with test_app.app_context():
        product = Product.query.get(sample_product)
        assert product is not None
        response = client.get(f'/products/{product.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Sample Product'
        assert data['description'] == 'This is a sample product.'
        assert data['price'] == 19.99
        assert data['stock'] == 100

def test_get_nonexistent_product(client):
    """
    Tests retrieving a product that doesn't exist.
    """
    response = client.get('/products/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None  # Ensure response body is not None
    assert data['msg'] == 'Product not found'


def test_add_product_as_admin(client, admin_token):
    """
    Tests adding a new product as an admin.
    """
    new_product = {
        'name': 'New Product',
        'description': 'A brand new product.',
        'price': 29.99,
        'stock': 50
    }
    response = client.post(
        '/products',
        json=new_product,
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['msg'] == 'Product added'
    assert 'product_id' in data

    # Verify that the product was added
    with client.application.app_context():
        product = Product.query.get(data['product_id'])
        assert product is not None
        assert product.name == 'New Product'

def test_add_product_as_non_admin(client, user_token):
    """
    Tests adding a new product as a non-admin user.
    """
    new_product = {
        'name': 'Unauthorized Product',
        'description': 'Should not be added.',
        'price': 9.99,
        'stock': 10
    }
    response = client.post(
        '/products',
        json=new_product,
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data['msg'] == 'Admin privilege required'

def test_add_product_missing_fields(client, admin_token):
    """
    Tests adding a new product with missing required fields.
    """
    incomplete_product = {
        'description': 'Missing name and price.'
    }
    response = client.post(
        '/products',
        json=incomplete_product,
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['msg'] == 'Name and price are required fields'

def test_edit_product_as_admin(client, admin_token, sample_product):
    """
    Tests editing an existing product as an admin.
    """
    updated_data = {
        'name': 'Updated Product',
        'price': 24.99,
        'stock': 80
    }
    response = client.put(
        f'/products/{sample_product.id}',
        json=updated_data,
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['msg'] == 'Product updated'
    assert data['product_id'] == sample_product.id

    # Verify that the product was updated
    with client.application.app_context():
        product = Product.query.get(sample_product.id)
        assert product.name == 'Updated Product'
        assert product.price == 24.99
        assert product.stock == 80

def test_edit_product_as_non_admin(client, user_token, sample_product):
    """
    Tests editing a product as a non-admin user.
    """
    updated_data = {
        'name': 'Hacked Product',
        'price': 0.99
    }
    response = client.put(
        f'/products/{sample_product.id}',
        json=updated_data,
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data['msg'] == 'Admin privilege required'

def test_edit_product_no_data(client, admin_token, sample_product):
    """
    Tests editing a product without providing any data.
    """
    response = client.put(
        f'/products/{sample_product.id}',
        json=None,
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['msg'] == 'No data provided'

def test_delete_product_as_admin(client, admin_token, sample_product):
    """
    Tests deleting a product as an admin.
    """
    response = client.delete(
        f'/products/{sample_product.id}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['msg'] == 'Product deleted'

    # Verify that the product was deleted
    with client.application.app_context():
        product = Product.query.get(sample_product.id)
        assert product is None

def test_delete_product_as_non_admin(client, user_token, sample_product):
    """
    Tests deleting a product as a non-admin user.
    """
    response = client.delete(
        f'/products/{sample_product.id}',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data['msg'] == 'Admin privilege required'

def test_delete_nonexistent_product(client, admin_token):
    """
    Tests deleting a product that doesn't exist.
    """
    response = client.delete(
        '/products/999',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 404
    data = response.get_json()
    assert data['msg'] == 'Product not found'