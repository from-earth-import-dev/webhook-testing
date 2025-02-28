import threading
import time

import pytest
from flask import Flask, jsonify, request
from werkzeug.serving import make_server

from app import trigger_alert
from models import WebhookPayload


@pytest.fixture(scope="module")
def customer_server():
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
        list: A list of received webhook payloads that can be inspected in tests
              to verify the correct WebhookPayload data was sent.

    Cleanup:
        The server is automatically shutdown and the thread joined when the
        fixture goes out of scope.
    """
    customer_app = Flask("customer_app")
    received_alerts = []

    @customer_app.route("/client-webhook", methods=["POST"])
    def client_webhook():
        data = request.get_json()
        received_alerts.append(data)
        return jsonify({"status": "received"}), 200

    server = make_server("127.0.0.1", 5001, customer_app)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    yield received_alerts
    server.shutdown()
    thread.join()


def test_alert_triggers_client_post(customer_server):
    valid_payload_obj = WebhookPayload(
        event_id=789,
        timestamp="2023-10-05T12:34:56",
        event_type="alert",
        description="Customer endpoint test",
    )
    target_url = "http://127.0.0.1:5001/client-webhook"
    start_time = time.perf_counter()
    response = trigger_alert(valid_payload_obj, target_url)
    response_time = time.perf_counter() - start_time

    # Validate that the POST request was successful.
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"

    # Wait briefly to ensure the dummy endpoint processed the request.
    time.sleep(0.1)

    assert len(customer_server) == 1, "Expected exactly one alert"
    received_data = customer_server[0]
    assert (
        received_data["event_id"] == valid_payload_obj.event_id
    ), "Received alert should match the expected payload"
    assert response_time < 0.5, "Response time should be less than 0.5 seconds"
