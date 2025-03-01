# Webhook Event Processing System

This project implements a simple webhook event processing system with two main components:

1. A Flask server that receives webhook events
2. A mechanism to trigger outgoing alerts to client endpoints

## Project Overview

The system validates incoming webhook payloads against a Pydantic model, stores valid events in memory, and provides functionality to forward events to client endpoints. This is particularly useful for event-driven architectures, notification systems, or any application that needs to process and relay webhook events.

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `app.py`: Main Flask application with webhook endpoint and alert trigger functionality
- `models.py`: Pydantic models for data validation
- `test_webhook.py`: Tests for the webhook functionality
- `.flake8`: Flake8 configuration for code linting
- `.pre-commit-config.yaml`: Pre-commit hooks configuration for code quality

## Running the Application

Start the Flask server:
```bash
python app.py
```

The server will run on `http://127.0.0.1:5000` by default with the following endpoint:

- `POST /webhook`: Accepts webhook event payloads

## Webhook Payload Format

The webhook endpoint expects JSON payloads with the following structure:

```json
{
  "event_id": 123,
  "timestamp": "2023-10-05T12:34:56",
  "event_type": "notification",
  "description": "Event description"
}
```

## Triggering Alerts

The system can forward events to client endpoints using the `trigger_alert` function:

```python
from app import trigger_alert
from models import WebhookPayload

payload = WebhookPayload(
    event_id=123,
    timestamp="2023-10-05T12:34:56",
    event_type="alert",
    description="Important notification"
)

response = trigger_alert(payload, "https://client-endpoint.example.com/webhook")
```

## Testing

Run the tests using pytest:

```bash
pytest
```

The test suite includes a mock customer server that validates the full webhook flow, ensuring that events are properly received, validated, and forwarded.

## Development

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Code linting
- **MyPy**: Static type checking
- **Pre-commit hooks**: Automated checks before committing

To set up pre-commit hooks:

```bash
pre-commit install
```

## Use Cases

- Event notification systems
- Monitoring and alerting pipelines
- Integration between microservices
- Webhook relay/proxy services
- Testing webhook integrations
