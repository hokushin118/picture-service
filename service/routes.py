"""
Picture Routes.

This microservice handles the application pictures.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Request
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_200_OK

from service import NAME, VERSION, BASE_DIR
from service.schemas import InfoDTO, HealthCheckDTO, IndexDTO

logger = logging.getLogger(__name__)

ROOT_PATH = '/api'
HEALTH_PATH = f"{ROOT_PATH}/health"
INFO_PATH = f"{ROOT_PATH}/info"
ACCOUNTS_PATH_V1 = f"{ROOT_PATH}/v1/pictures"

router = APIRouter(
    prefix='',
    tags=['General']
)

# --- Templates ---
# Mount the Jinja2 template files directory
# The Jinja2 template files directory contains the microservice's HTML files
# https://fastapi.tiangolo.com/advanced/templates/
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))


######################################################################
# HOME PAGE
######################################################################
@router.get(
    '/',
    name='general:home',
    response_class=HTMLResponse,
    response_model=None,
    status_code=HTTP_200_OK,
    summary='Display Microservice Home Page',
    description='Serves the main HTML landing page for the microservice. '
                'Requires Jinja2 templates to be configured and an '
                '`index.html` file in the templates directory.',
    response_description='The HTML content of the microservice home page.',
    tags=['General']
)
async def home(
        request: Request
) -> Jinja2Templates.TemplateResponse:
    """Serves the microservice's primary HTML home page (`index.html`).

    This endpoint renders the main landing page using the configured Jinja2
    template engine. The `index.html` file must be located in the
    application's designated 'templates' directory.

    Reference: https://fastapi.tiangolo.com/advanced/templates/

    Args:
        request: The incoming FastAPI request object. This is automatically
                 injected by FastAPI and is required by `TemplateResponse`
                 to generate URLs correctly within the template.

    Returns:
        TemplateResponse: An HTML response rendered from the `index.html`
                          template, including the necessary request context.
    """
    return templates.TemplateResponse(
        name='index.html',
        context={
            'request': request
        }
    )


######################################################################
# GET INDEX
######################################################################
@router.get(
    ROOT_PATH,
    name='general:index',
    response_model=IndexDTO,
    status_code=HTTP_200_OK,
    summary='Returns a welcome message for the Picture API',
    description='It always returns a 200 OK status with the message: '
                '"Welcome to the Picture API".</br></br>'
                'This endpoint is accessible to anonymous users.',
    response_description='Welcome message for the API',
    tags=['General']
)
async def index() -> IndexDTO:
    """Returns a welcome message for the API.

    This operation can be performed by an unauthenticated user. It is an
    asynchronous and idempotent method.

    Returns:
        IndexDTO: Welcome message.
    """
    return IndexDTO(
        message='Welcome to the Picture API!'
    )


############################################################
# GET HEALTH
############################################################
@router.get(
    HEALTH_PATH,
    name='general:health',
    response_model=HealthCheckDTO,
    status_code=HTTP_200_OK,
    summary='Returns the health status of the service',
    description='Checks the overall health of the service. Currently, '
                'it always returns a 200 OK status with a "status: UP" '
                'message.</br></br>This endpoint is accessible to '
                'anonymous users.',
    response_description='Health status of the service',
    tags=['General']
)
async def health() -> HealthCheckDTO:
    """Performs a health check of the application.

    This operation can be performed by an unauthenticated user. It is an
    asynchronous and idempotent method.

    Returns:
        HealthCheckDTO: Health status of the service.
        The status is always "UP".
    """
    return HealthCheckDTO(
        status='UP'
    )


############################################################
# GET INFO
############################################################
@router.get(
    INFO_PATH,
    name='general:info',
    response_model=InfoDTO,
    status_code=HTTP_200_OK,
    summary='Returns information about the service',
    description='Provides information about the service, '
                'including its name, version, and uptime.</br></br>'
                'This endpoint is accessible to anonymous users.',
    response_description='Information about the service',
    tags=['General']
)
async def version(request: Request) -> InfoDTO:
    """Retrieves the current version of the application.

    This operation can be performed by an unauthenticated user. It is an
    asynchronous and idempotent method.

    Args:
        request (Request): The incoming request object.  Used to access the
            application's state.

    Returns:
        InfoDTO: Information about the service, including name, version,
        and uptime.
    """
    uptime = 'Not yet started'
    start_time = getattr(request.app.state, 'start_time', None)
    if start_time and isinstance(start_time, datetime):
        uptime_delta = datetime.now(timezone.utc) - start_time
        uptime = str(uptime_delta)
    elif start_time:
        uptime = "Error: Invalid start_time format in app state"

    return InfoDTO(
        name=NAME,
        version=VERSION,
        uptime=uptime,
    )
