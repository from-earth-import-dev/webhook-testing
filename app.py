from flask import Flask

from webhook_service.app import create_app

# Create the Flask application
app: Flask = create_app()

if __name__ == "__main__":
    app.run(debug=True)
