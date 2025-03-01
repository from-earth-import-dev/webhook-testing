"""Common test fixtures for webhook service tests."""
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from webhook_service.app import create_app
from webhook_service.routes import triggered_events


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create a Flask app for testing."""
    app = create_app({"TESTING": True})
    yield app
    # Clear triggered events after each test
    triggered_events.clear()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the app."""
    return app.test_client()
