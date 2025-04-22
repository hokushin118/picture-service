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
from starlette.status import HTTP_200_OK

from service import NAME, VERSION
from service.schemas import InfoDTO, HealthCheckDTO

logger = logging.getLogger(__name__)

ROOT_PATH = '/api'
HEALTH_PATH = f"{ROOT_PATH}/health"
INFO_PATH = f"{ROOT_PATH}/info"
ACCOUNTS_PATH_V1 = f"{ROOT_PATH}/v1/pictures"

router = APIRouter(
    prefix='',
    tags=['General']
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
    tags=['General'])
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
@router.get(INFO_PATH,
            name='general:info',
            response_model=InfoDTO,
            status_code=HTTP_200_OK,
            summary='Returns information about the service',
            description='Provides information about the service, '
                        'including its name, version, and uptime.</br></br>'
                        'This endpoint is accessible to anonymous users.',
            response_description='Information about the service',
            tags=['General'])
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
