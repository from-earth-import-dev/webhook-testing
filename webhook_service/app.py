from typing import Any, Dict, Optional

from flask import Flask

from webhook_service.routes import register_routes


def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:
    """Create and configure the Flask application."""
    app: Flask = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.update(test_config)

    register_routes(app)

    return app


# For direct execution
if __name__ == "__main__":
    app: Flask = create_app()
    app.run(debug=True)
