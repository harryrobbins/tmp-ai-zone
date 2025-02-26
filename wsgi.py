"""
WSGI entry point for the application.
This allows the app to be run by WSGI containers like Gunicorn or uWSGI.
"""
from app import app

if __name__ == "__main__":
    # For local development
    app.run(host='0.0.0.0', port=8000)