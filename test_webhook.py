import threading
import time
from datetime import datetime
from typing import Generator

import pytest
from flask import Flask, Response, jsonify, request
from werkzeug.serving import make_server

from app import trigger_alert
from models import WebhookPayload


@pytest.fixture(scope="module")
def customer_server() -> Generator[list[dict], None, None]:
    """
    Creates a test Flask server that simulates a customer's webhook endpoint.

    This fixture runs a Flask server in a background thread on port 5001 that acts as
    a mock customer endpoint. It's used to validate the webhook flow in app.py where
    WebhookPayload events trigger outgoing POST requests.

    The server exposes a /client-webhook endpoint that:
    - Accepts POST requests with JSON payloads
    - Stores received payloads in memory
    - Returns a 200 status with {"status": "received"}

    Yields:
        Generator: A generator yielding a list of received webhook payloads that can
            be inspected in tests to verify the correct WebhookPayload data was sent.

    Cleanup:
        The server is automatically shutdown and the thread joined when the
        fixture goes out of scope.
    """
    customer_app = Flask("customer_app")
    received_alerts: list[dict] = []

    @customer_app.route("/client-webhook", methods=["POST"])
    def client_webhook() -> Response:
        data = request.get_json()
        received_alerts.append(data)
        return jsonify({"status": "received"}), 200

    server = make_server("127.0.0.1", 5001, customer_app)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    yield received_alerts
    server.shutdown()
    thread.join()


def test_alert_triggers_client_post(customer_server: list[dict]) -> None:
    """
    This test validates that triggering an alert sends a valid POST request
    to a simulated client's webhook endpoint. It ensures that the event data
    is correctly transmitted, processed by the receiving endpoint, and meets
    the required performance benchmarks.

    Checks:
    1. Verify that the HTTP response status code is 200.
    2. Confirm that the response JSON contains a "status" key with the value "received".
    3. Ensure that the dummy customer server receives exactly one alert.
    4. Check that the received alert payload's event_id matches the expected value.
    5. Validate that the response time is less than 0.5 seconds.
    """
    valid_payload_obj = WebhookPayload(
        event_id=789,
        timestamp=datetime.now(),
        event_type="alert",
        description="Customer endpoint test",
    )
    target_url = "http://127.0.0.1:5001/client-webhook"
    start_time = time.perf_counter()
    response = trigger_alert(valid_payload_obj, target_url)
    response_time = time.perf_counter() - start_time

    # (1) Verify that the HTTP response status code is 200.
    assert response.status_code == 200

    # (2) Confirm that the response JSON contains a "status" key with the correct value.
    data = response.json()
    assert data["status"] == "received"

    # (3) Ensure that the dummy customer server receives exactly one alert.
    # Wait briefly to ensure the dummy endpoint processed the request.
    time.sleep(0.1)
    assert len(customer_server) == 1, "Expected exactly one alert"

    # (4) Check that the received alert payload's event_id matches the expected value.
    received_data = customer_server[0]
    assert (
        received_data["event_id"] == valid_payload_obj.event_id
    ), "Received alert should match the expected payload"

    # (5) Validate that the response time is less than 0.5 seconds.
    assert response_time < 0.5, "Response time too high"
