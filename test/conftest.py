# tests/conftest.py

import os
import sys
import pytest
import sqlite3
from fastapi.testclient import TestClient

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, get_db

import logging
logger = logging.getLogger('main')

@pytest.fixture(scope="module")
def test_db():
    """Fixture for setting up an in-memory database."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    with open(f'sql/groups_users.ddl', 'r', encoding='utf8') as sqlfile:
        sqldata = sqlfile.read()
        cursor.executescript(sqldata)

    conn.commit()
    
    yield conn  # This will be the test database during the tests
    
    conn.close()  # Close the connection after tests


@pytest.fixture
def client(test_db):
    """Fixture for creating a TestClient instance."""
    # Override the get_db function to use the in-memory database
    def override_get_db():
        logger.warning("Calling test db")
        return test_db

    app.dependency_overrides[get_db] = override_get_db
    conn = get_db()
    yield TestClient(app)  # Provide the FastAPI TestClient instance

    # Cleanup dependency overrides
    app.dependency_overrides = {}
