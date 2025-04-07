"""
Package: main
This package configures the FastAPI application, and sets up service routes.

It also handles application-level logging.
"""
from __future__ import annotations

import os

from fastapi import FastAPI

# Retrieving Information (Environment Variables Example):
# This is a common way to manage configuration, especially in containerized environments.
VERSION = os.environ.get('VERSION', '0.0.1')  # Default if not set
NAME = os.environ.get('NAME', 'REST API Service for Pictures')


# --- FastAPI Application Setup ---
def create_app() -> FastAPI:
    """Creates and configures a FastAPI application instance.

    This factory function initializes a FastAPI application, applies configuration
    settings from the specified configuration object, and returns the configured
    application.

    Returns:
        FastAPI: A configured FastAPI application instance.
    """

    current_app = FastAPI(
        title=NAME,
        version=VERSION
    )
    return current_app


# --- Application Initialization ---
# Swagger: http://127.0.0.1:8000/docs auto generated
# Redoc: http://127.0.0.1:8000/redoc
app = create_app()
