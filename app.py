import requests
from flask import Flask, Response, jsonify, request
from pydantic import ValidationError

from models import WebhookPayload

app = Flask(__name__)
triggered_events = []


@app.route("/webhook", methods=["POST"])
def webhook() -> Response:
    """
    Webhook endpoint that receives and validates event payloads.

    This endpoint is used in conjunction with test_webhook.py which validates the
    full webhook flow. It receives POST requests containing event data, validates
    them against the WebhookPayload model, and stores valid events in memory.

    The endpoint expects a JSON payload matching the WebhookPayload schema with:
    - event_id (int): Unique identifier for the event
    - timestamp (datetime): ISO 8601 formatted timestamp
    - event_type (str): Type of event
    - description (str): Event description

    Returns:
        200: JSON response with status="success" and event_id if validation passes
        400: JSON response with status="error" if payload is invalid
        500: JSON response with status="error" for unexpected errors
    """
    data = request.get_json()

    if data is None:
        return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

    try:
        payload = WebhookPayload(**data)
        triggered_events.append(payload)
        return jsonify({"status": "success", "event_id": payload.event_id}), 200

    except ValidationError as e:
        return jsonify({"status": "error", "errors": e.errors()}), 400

    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


def trigger_alert(payload: WebhookPayload, target_url: str) -> requests.Response:
    """
    Trigger an outgoing alert POST request to the customer.
    """
    response = requests.post(target_url, json=payload.model_dump(mode="json"))
    return response


if __name__ == "__main__":
    app.run(debug=True)
