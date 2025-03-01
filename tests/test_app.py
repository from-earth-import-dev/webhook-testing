import json
from datetime import datetime
from typing import Any, Dict

from flask.testing import FlaskClient

from webhook_service.routes import triggered_events


def test_webhook_valid_payload(client: FlaskClient) -> None:
    """Test that valid webhook payloads are accepted."""
    # Create a valid payload
    payload: Dict[str, Any] = {
        "event_id": 123,
        "timestamp": datetime.now().isoformat(),
        "event_type": "test",
        "description": "Test webhook",
    }

    # Send POST request to webhook endpoint
    response = client.post(
        "/webhook", data=json.dumps(payload), content_type="application/json"
    )

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert data["event_id"] == 123

    # Verify event was stored
    assert len(triggered_events) == 1
    assert triggered_events[0].event_id == 123


def test_webhook_invalid_payload(client: FlaskClient) -> None:
    """Test that invalid webhook payloads are rejected."""
    # Create an invalid payload (missing required fields)
    payload: Dict[str, Any] = {
        "event_id": 123,
        # Missing timestamp
        "event_type": "test"
        # Missing description
    }

    # Send POST request to webhook endpoint
    response = client.post(
        "/webhook", data=json.dumps(payload), content_type="application/json"
    )

    # Check response
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["status"] == "error"

    # Verify no event was stored
    assert len(triggered_events) == 0
