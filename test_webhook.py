import time
import threading
import pytest
from werkzeug.serving import make_server
from app import trigger_alert
from models import WebhookPayload
from flask import Flask, request, jsonify

# Pytest fixture to create a dummy customer webhook endpoint.
# It runs the Flask server in a background thread on port 5001 and yields
# the list of received alert payloads.
@pytest.fixture(scope="module")
def customer_server():
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

# End-to-end test that validates that the Meter's alert triggers an outgoing POST
# to the customer's webhook endpoint with the expected payload and response time.
def test_alert_triggers_client_post(customer_server):
    valid_payload_obj = WebhookPayload(
        event_id=789,
        timestamp="2023-10-05T12:34:56",  # ISO 8601 format
        event_type="alert",
        description="Customer endpoint test"
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
    # Validate that the endpoint received one alert with the expected event_id.
    assert len(customer_server) == 1
    received_data = customer_server[0]
    assert received_data["event_id"] == valid_payload_obj.event_id
    # Validate that the response time is within an acceptable threshold.
    assert response_time < 0.5 