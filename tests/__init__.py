"""
conftest.py

This module contains unit tests for the application.

It sets up the testing environment by providing fixtures and configurations 
necessary for running tests. This includes the creation of a test client 
for making requests and managing the database setup and teardown.

Main Functionality:
- Provides a test client fixture that sets up the application context 
  and database schema for testing purposes.
- Ensures that the database is created before tests run and dropped 
  after tests complete, maintaining a clean state for each test module.

Usage:
To use this module, simply place your test files in the same directory 
or a subdirectory. The fixtures defined here will be automatically 
available to your tests.

Example:
    def test_example(test_client):
        response = test_client.get('/some-endpoint')
        assert response.status_code == 200
"""

import logging
import pytest
from app import create_app
from app.models import db
from config import TestConfig

# Configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="module")
def test_client():
    """
    Fixture for creating a test client for the application.

    Sets up the application and creates a test client for making requests.
    Also sets up and tears down the database schema for testing.

    Returns:
        FlaskClient: The test client instance.
    """
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()
