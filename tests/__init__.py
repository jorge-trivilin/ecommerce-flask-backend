"""
Unit tests for the application.

This module contains fixtures and configurations for setting up the testing environment,
including database setup and client configuration for testing purposes.
"""

import logging
import pytest
from app import create_app
from app.models import db

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
    app = create_app("config.TestingConfig")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()
