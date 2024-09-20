"""
Test configuration and fixtures for the Flask application.

This module sets up the testing environment for the Flask application. It provides
fixtures and configurations necessary for running tests, including database setup
and teardown.

Key components:
- Logging configuration: Sets up logging for debugging test execution.
- test_client fixture: Creates a Flask test client with a test database for each test module.

The module uses pytest for test management and Flask's testing utilities for creating
a test client. It also manages the database lifecycle, creating tables before tests
and dropping them after tests are complete.

Usage:
    This module is automatically used by pytest when running tests. The fixtures
    defined here are available to all test files in the same directory or subdirectories.

Example:
    To use the test client in a test file:

    def test_some_route(test_client):
        response = test_client.get('/some-route')
        assert response.status_code == 200

Note:
    Make sure that the TestConfig is properly set up in the config.py file to use
    a test-specific database (e.g., an in-memory SQLite database).
"""

import logging
import pytest
from app import create_app
from app.models import db
from config import TestConfig

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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
