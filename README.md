# Webhook Event Processing System

This project implements a simple webhook event processing system with two main components:

1. A Flask server that receives webhook events
2. A mechanism to trigger outgoing alerts to client endpoints

## Project Overview

The system validates incoming webhook payloads against a Pydantic model, stores valid events in memory, and provides functionality to forward events to client endpoints. This is particularly useful for event-driven architectures, notification systems, or any application that needs to process and relay webhook events.

## Project Structure

The project follows best practices for Python package organization:

```
webhook_testing/
├── webhook_service/       # Main package
│   ├── app.py             # Flask application setup
│   ├── models.py          # Data models
│   └── routes.py          # API endpoints
├── tests/                 # Test directory
│   ├── test_app.py        # App & endpoint tests
│   └── test_webhook.py    # Webhook integration tests
├── app.py                 # Application entry point
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

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

## Code Quality

This project maintains high code quality through:

- **Type Hints**: Comprehensive type annotations using Python's typing module
- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Code linting
- **MyPy**: Static type checking for verifying type hints
- **Pre-commit hooks**: Automated checks before committing

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
from webhook_service.routes import trigger_alert
from webhook_service.models import WebhookPayload
from datetime import datetime

payload = WebhookPayload(
    event_id=123,
    timestamp=datetime.now(),
    event_type="alert",
    description="Important notification"
)

response = trigger_alert(payload, "https://client-endpoint.example.com/webhook")
```

## Testing

Run the tests locally using pytest:

```bash
pytest
```

In addition, this project is integrated with GitHub Actions. The CI workflow defined in
`.github/workflows/python-tests.yml` automatically runs the tests on every push, pull request (to the main branch), and can also be triggered manually via the `workflow_dispatch` event.

To view the workflow runs and logs, visit the [GitHub Actions](https://github.com/<your_org>/<your_repo>/actions) tab in your repository.

## Development

To set up pre-commit hooks:

```bash
pre-commit install
```
