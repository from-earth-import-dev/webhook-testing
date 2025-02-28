from flask import Flask, request, jsonify
from pydantic import ValidationError
from models import WebhookPayload

app = Flask(__name__)
# Global list to simulate triggered events for testing purposes
triggered_events = []

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data is None:
        # If no JSON is provided, return an error message.
        return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400
    try:
        # Validate the payload using the Pydantic model.
        payload = WebhookPayload(**data)
        # Simulate event triggering by storing the payload.
        triggered_events.append(payload)
        return jsonify({"status": "success", "event_id": payload.event_id}), 200
    except ValidationError as e:
        # Return a response with the error details.
        return jsonify({"status": "error", "errors": e.errors()}), 400
    except Exception as exc:
        # For any other errors, return a 500 response.
        return jsonify({"status": "error", "message": str(exc)}), 500

# New function to trigger an outgoing alert POST request (Meter sending alert to customer)
def trigger_alert(payload: WebhookPayload, target_url: str):
    import requests  # Import here to keep dependencies local to this functionality.
    # Convert the payload to a dict and send the POST request.
    response = requests.post(target_url, json=payload.dict())
    return response

if __name__ == '__main__':
    app.run(debug=True) 