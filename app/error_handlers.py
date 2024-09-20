"""
error_handlers.py

This module defines custom error handlers for the Flask application.
It registers handlers for various HTTP exceptions and general exceptions,
providing a consistent format for error responses and logging error messages.

Main Functionality:
- Registers error handlers for common HTTP status codes:
  - 400 Bad Request
  - 404 Not Found
  - 405 Method Not Allowed
  - 500 Internal Server Error
- Handles generic exceptions to ensure that all errors are logged
  and returned in a standardized JSON format.

Usage:
To use this module, call the `register_error_handlers(app)` function
with the Flask app instance. This will set up the error handling
mechanism for the application.

Example:
    from app.error_handlers import register_error_handlers

    app = Flask(__name__)
    register_error_handlers(app)

"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """
    Registers custom error handlers with the Flask app.
    These handlers are used to format error responses and
    log error messages for different HTTP status codes.
    """

    @app.errorhandler(Exception)
    def handle_exception(e):  # pylint: disable=unused-argument
        # Handle specific HTTP exceptions
        if isinstance(e, HTTPException):
            return jsonify({"error": e.name, "message": e.description}), e.code

        # Handle other exceptions
        app.logger.error(f"An unhandled exception occurred: {str(e)}")
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                }
            ),
            500,
        )

    @app.errorhandler(400)
    def bad_request(e):  # pylint: disable=unused-argument
        return jsonify(
            {"error": "Bad Request", "message": str(e.description)}), 400

    @app.errorhandler(404)
    def not_found(e):  # pylint: disable=unused-argument
        return (
            jsonify(
                {
                    "error": "Not Found",
                    "message": "The requested resource was not found",
                }
            ),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(e):  # pylint: disable=unused-argument
        return (
            jsonify(
                {
                    "error": "Method Not Allowed",
                    "message": "The method is not allowed for the requested URL",
                }),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(e):  # pylint: disable=unused-argument
        app.logger.error(f"An internal server error occurred: {str(e)}")
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                }
            ),
            500,
        )
