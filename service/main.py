"""
Package: main
This package configures the FastAPI application, and sets up service routes.

It also handles application-level logging.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import FastAPI

from service import app_config, NAME, VERSION
from service.routes import router

logger = logging.getLogger(__name__)


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
        title=app_config.description,
        version=app_config.version
    )

    # Adding routes
    current_app.include_router(router)

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
