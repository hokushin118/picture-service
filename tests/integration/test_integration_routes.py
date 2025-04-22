"""
Routes Integration Test Suite.

Test cases can be run with the following:
  pytest -v --with-integration --log-cli-level=DEBUG tests/integration
"""
import asyncio
import logging
import pathlib
import time
from typing import AsyncGenerator

import httpx
import pytest
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from service import NAME, VERSION
from service.routes import HEALTH_PATH, INFO_PATH, ROOT_PATH
from tests.integration import ensure_url, join_urls

# Find the project root directory (where Dockerfile is located)
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent

# Image name to build
TEST_IMAGE_NAME = 'fastapi-picture-service-test:latest'

# Internal port the service listens on inside the container
SERVICE_PORT = 5000

logger = logging.getLogger(__name__)


############################################################
# FIXTURES
############################################################
@pytest.fixture(scope='session')
async def service_container() -> AsyncGenerator[str, None]:
    """Builds and runs the FastAPI service Docker container for
    integration tests.

    Yields:
        str: The base URL (http://host:port) where the service is accessible.
    """
    logger.info(
        "Building image '%s' from Dockerfile at '%s'",
        TEST_IMAGE_NAME,
        PROJECT_ROOT
    )

    # Build the image first
    import subprocess  # pylint: disable=C0415
    try:
        subprocess.run(
            ['docker', 'build', '-t', TEST_IMAGE_NAME, '.'],
            cwd=str(PROJECT_ROOT),
            check=True,
            capture_output=True
        )
        logger.info('Docker image built successfully...')
    except subprocess.CalledProcessError as err:
        logger.error(
            "Failed to build Docker image: %s",
            err.stderr.decode()
        )
        raise

    # Create and configure the container
    container = DockerContainer(image=TEST_IMAGE_NAME)
    container.with_exposed_ports(SERVICE_PORT)
    container.with_env('ENVIRONMENT', 'testing')

    logger.info('Starting container...')

    with container as running_container:
        host = running_container.get_container_host_ip()
        port = running_container.get_exposed_port(SERVICE_PORT)
        # Ensure the base_url includes the protocol
        base_url = ensure_url(f"{host}:{port}")
        logger.info(
            "Service container started. Base URL: %s",
            base_url
        )

        # Wait for service readiness
        try:
            # Wait for uvicorn startup message
            wait_for_logs(
                running_container,
                r"Application startup complete.",
                timeout=60
            )
            logger.info(
                "Detected 'Application startup complete.' log."
            )
        except TimeoutError:
            logger.warning(
                'Did not detect startup log message within timeout.'
            )

            # Fallback to health check
            logger.info(
                "Attempting readiness check via %s endpoint...",
                HEALTH_PATH
            )
            max_wait = 60
            start_wait = time.time()
            ready = False

            async with httpx.AsyncClient() as client:
                while time.time() - start_wait < max_wait:
                    try:
                        # Ensure the health check URL includes the protocol
                        health_url = join_urls(base_url, HEALTH_PATH)
                        logger.debug(
                            "Attempting health check at: %s",
                            health_url
                        )
                        response = await client.get(health_url, timeout=2)
                        if response.status_code == HTTP_200_OK and response.json().get(
                                'status'
                        ) == 'UP':
                            logger.info(
                                "%s check successful.",
                                HEALTH_PATH
                            )
                            ready = True
                            break
                    except (
                            httpx.ConnectError,
                            httpx.TimeoutException,
                            httpx.ReadError
                    ) as err:
                        logger.debug(
                            "Health check failed: %s, retrying...",
                            err
                        )
                    await asyncio.sleep(1)

            if not ready:
                # Dump logs if readiness check fails
                logs = running_container.get_logs()[0].decode().strip() if \
                    running_container.get_logs()[0] else ''
                logs_stderr = running_container.get_logs()[1].decode().strip() \
                    if running_container.get_logs()[1] else ''
                logger.error(
                    "Service readiness check failed after %s.\nSTDOUT:\n%s\nSTDERR:\n%s",
                    max_wait,
                    logs,
                    logs_stderr
                )
                pytest.fail(
                    f"Service did not become ready at {base_url}{HEALTH_PATH}"
                )

        yield base_url

    logger.info('Service container stopped.')


############################################################
# INTEGRATION TESTS SCENARIOS
############################################################
@pytest.mark.integration
class TestGeneralEndpointIntegration:
    """The General Endpoints Integration Tests."""

    @pytest.mark.asyncio
    async def test_home_endpoint(
            self,
            service_container: AsyncGenerator[str, None]
    ):
        """It should test the microservice home page for a
        successful response."""
        async for base_url in service_container:
            # Ensure the home URL includes the protocol
            health_url = join_urls(base_url, '/')
            logger.info(
                "Testing home page: %s",
                health_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(health_url)

                assert response.status_code == HTTP_200_OK
                assert response.headers[
                           'Content-Type'
                       ] == 'text/html; charset=utf-8'
            break

    @pytest.mark.asyncio
    async def test_root_endpoint(
            self,
            service_container: AsyncGenerator[str, None]
    ):
        """It should test the /api endpoint for a
        successful response."""
        async for base_url in service_container:
            # Ensure the root URL includes the protocol
            health_url = join_urls(base_url, ROOT_PATH)
            logger.info(
                "Testing root endpoint: %s",
                health_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(health_url)

                assert response.status_code == HTTP_200_OK
                assert response.headers['Content-Type'] == 'application/json'
                assert response.json() == {
                    'message': 'Welcome to the Picture API!'
                }
            break

    @pytest.mark.asyncio
    async def test_health_endpoint(
            self,
            service_container: AsyncGenerator[str, None]
    ):
        """It should test the /api/health endpoint for a
        successful response."""
        async for base_url in service_container:
            # Ensure the health URL includes the protocol
            health_url = join_urls(base_url, HEALTH_PATH)
            logger.info(
                "Testing health endpoint: %s",
                health_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(health_url)

                assert response.status_code == HTTP_200_OK
                assert response.headers['Content-Type'] == 'application/json'
                assert response.json() == {'status': 'UP'}
            break

    @pytest.mark.asyncio
    async def test_info_endpoint(
            self,
            service_container: AsyncGenerator[str, None]
    ):
        """It should test the /api/info endpoint for correct
        structure and data."""
        async for base_url in service_container:
            # Ensure the info URL includes the protocol
            info_url = join_urls(base_url, INFO_PATH)
            logger.info(
                "Testing info endpoint: %s",
                info_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(info_url)

                assert response.status_code == HTTP_200_OK
                assert response.headers['Content-Type'] == 'application/json'

                data = response.json()
                assert isinstance(data, dict)

                assert data.get('name') == NAME
                assert data.get('version') == VERSION
                assert 'uptime' in data
                assert isinstance(data['uptime'], str)
                assert data['uptime'] != 'Not yet started'
                assert 'Error:' not in data['uptime']
                assert (':' in data['uptime'] or 'day' in data['uptime'])
            break

    @pytest.mark.asyncio
    async def test_invalid_endpoint(
            self,
            service_container: AsyncGenerator[str, None]
    ):
        """It should test handling of invalid endpoints."""
        async for base_url in service_container:
            # Ensure the invalid URL includes the protocol
            invalid_url = join_urls(base_url, 'api/nonexistent')
            logger.info(
                "Testing invalid endpoint: %s",
                invalid_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(invalid_url)

                assert response.status_code == HTTP_404_NOT_FOUND
                assert response.headers['Content-Type'] == 'application/json'
                assert 'detail' in response.json()
            break

    @pytest.mark.asyncio
    async def test_service_headers(
            self,
            service_container: AsyncGenerator[str, None]
    ):
        """It should test that the service returns appropriate security
        headers."""
        async for base_url in service_container:
            # Ensure the health URL includes the protocol
            health_url = join_urls(base_url, HEALTH_PATH)
            logger.info(
                "Testing service headers: %s",
                health_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(health_url)

                assert 'X-Content-Type-Options' in response.headers
                assert 'X-Frame-Options' in response.headers
                assert 'X-XSS-Protection' in response.headers
            break
