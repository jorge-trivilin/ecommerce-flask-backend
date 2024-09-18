# tests/__init__.py

import pytest
import logging
from app import create_app
from app.models import db

logging.basicConfig(level=logging.DEBUG)

@pytest.fixture(scope='module')
def test_client():
    app = create_app('config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture(scope='module')
def init_db(test_client):
    pass
