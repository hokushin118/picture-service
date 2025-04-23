"""
Package: main
This package configures the FastAPI application, and sets up service routes.

It also handles application-level logging.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from cba_core_lib.utils.enums import UserRole
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from service import (
    app_config,
    NAME,
    VERSION,
    SWAGGER_ENABLED,
    BASE_DIR
)
from service.routes import router

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
        openapi_url=OPENAPI_URL if SWAGGER_ENABLED else None,

        # Standard paths for interactive API documentation UIs
        docs_url='/docs' if SWAGGER_ENABLED else None,  # Swagger UI path
        redoc_url='/redoc' if SWAGGER_ENABLED else None,  # ReDoc path

        # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
        swagger_ui_parameters={
            # Sort operations within tags alphabetically
            # by HTTP method (GET, POST, PUT ...)
            'operationsSorter': 'method'
        }
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
    current_app.include_router(router)
    logger.info('Application router included successfully.')

    return current_app


# --- Application Initialization ---
# Swagger: http://127.0.0.1:8000/docs auto generated
# Redoc: http://127.0.0.1:8000/redoc
app = create_app()


@app.on_event('startup')
async def startup() -> None:
    """Logs the successful startup of the application.

    This function is executed when the FastAPI application starts.
    It records the start time in the application state and logs an
    informational message containing the application name, version,
    and start time.

    Returns:
        None.  This function does not return any value.
    """
    app.state.start_time = datetime.now(timezone.utc)
    logger.info(
        "'%s' version '%s' started at %s",
        NAME,
        VERSION,
        app.state.start_time
    )


@app.on_event("shutdown")
async def shutdown():
    """Logs the shutdown of the application and the total uptime.

    This function is executed when the FastAPI application shuts down. It
    calculates the application's uptime (if the start time was recorded) and
    logs an informational message including the application name and its total
    uptime.

    Returns:
        None.  This function does not return a value.
    """
    start_time = getattr(app.state, 'start_time', None)
    uptime_str = "N/A"
    if start_time:
        uptime_str = str(datetime.now(timezone.utc) - start_time)
    logger.info(
        "'%s' shutting down. Total uptime: %s",
        NAME,
        uptime_str
    )
