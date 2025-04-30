"""
Package: main

This package configures the FastAPI application, and sets up service routers.

It also handles application-level logging.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from cba_core_lib.utils.enums import UserRole
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from service import (
    app_config,
    BASE_DIR
)
from service.routers.general import general_router
from service.routers.pictures import picture_router

logger = logging.getLogger(__name__)

OPENAPI_URL = '/openapi.json'
"""Path to the microservice description."""

# Metadata for organizing endpoints in the OpenAPI documentation UI
tags_metadata = [
    {
        'name': 'General',
        'description': 'General service information and '
                       'health check endpoints.'
    },
    {
        'name': 'Picture',
        'description': 'Endpoints related to picture management '
                       'and operations.'
    },
]


# --- Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(current_app: FastAPI):
    """Manages application startup and shutdown events.

    - On startup: Records the start time in app state and logs startup message.
    - On shutdown: Logs shutdown message including total uptime.
    """
    # --- Startup Logic ---
    start_time = datetime.now(timezone.utc)
    current_app.state.start_time = start_time  # Store start time in app state
    logger.info(
        "'%s' version '%s' starting up at %s...",
        app_config.name,
        app_config.version,
        start_time
    )

    yield

    # --- Shutdown Logic ---
    shutdown_time = datetime.now(timezone.utc)
    uptime_str = "N/A (start_time not found)"
    stored_start_time = getattr(current_app.state, 'start_time', None)
    if isinstance(stored_start_time, datetime):
        uptime_delta = shutdown_time - stored_start_time
        uptime_str = str(uptime_delta).split('.', maxsplit=1)[0]
    elif stored_start_time:
        logger.warning('Invalid start_time format found in app state.')

    logger.info(
        "'%s' shutting down. Total uptime: %s",
        app_config.name,
        uptime_str
    )


# --- FastAPI Application Setup ---
def create_app() -> FastAPI:
    """Creates and configures a FastAPI application instance.

    This factory function initializes a FastAPI application, applies configuration
    settings from the specified configuration object, and returns the configured
    application.

    Returns:
        FastAPI: A configured FastAPI application instance.
    """
    # Initialize the FastAPI application
    current_app = FastAPI(
        title=app_config.description,
        version=app_config.version,
        description=f'REST API for managing picture files and associated metadata.'
                    f'<br/><br/>_Python 3.9_, _MongoDB_<br/><br/>'
                    f'Test accounts data:<br/><br/>'
                    f'Login: **admin**<br/>'
                    f'Password: **test**<br/>'
                    f'Role: **{UserRole.ADMIN}**<br/><br/>'
                    f'Login: **test**<br/>'
                    f'Password: **test**<br/>'
                    f'Role: **{UserRole.USER}**',

        # OpenAPI tag metadata for grouping endpoints in docs
        openapi_tags=tags_metadata,

        # https://fastapi.tiangolo.com/how-to/conditional-openapi/#conditional-openapi-from-settings-and-env-vars
        # Conditionally enable/disable the OpenAPI schema endpoint
        # Useful for production environments if docs shouldn't be exposed.
        openapi_url=OPENAPI_URL if app_config.swagger_enabled else None,

        # Standard paths for interactive API documentation UIs
        # Swagger UI path
        docs_url='/docs' if app_config.swagger_enabled else None,
        # ReDoc path
        redoc_url='/redoc' if app_config.swagger_enabled else None,

        # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
        swagger_ui_parameters={
            # Sort operations within tags alphabetically
            # by HTTP method (GET, POST, PUT ...)
            'operationsSorter': 'method'
        },

        lifespan=lifespan
    )

    # Mount the static files directory
    # The static files directory contains the microservice's static files
    # (CSS files, JavaScript files, images, etc.)
    # https://fastapi.tiangolo.com/en/tutorial/static-files/
    current_app.mount(
        '/static',
        StaticFiles(
            directory=BASE_DIR / 'static'
        ),
        name='static'
    )

    # Include the main application router
    # This registers all the paths defined in the 'router' object
    current_app.include_router(general_router)
    current_app.include_router(picture_router)

    logger.info('Application router included successfully.')

    return current_app


# --- Application Initialization ---
# Swagger: http://127.0.0.1:8000/docs auto generated
# Redoc: http://127.0.0.1:8000/redoc
app = create_app()
