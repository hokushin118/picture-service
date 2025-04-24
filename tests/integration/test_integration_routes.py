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
from testcontainers.minio import MinioContainer
from testcontainers.mongodb import MongoDbContainer

from service import app_config
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
def mongo_container() -> MongoDbContainer:
    """Start MongoDB container for testing."""
    container = MongoDbContainer()
    with container as mongo:
        logger.info(
            "MongoDB container started at %s",
            mongo.get_connection_url()
        )
        yield mongo


@pytest.fixture(scope='session')
def minio_container() -> MinioContainer:
    """Start MinIO container for testing."""
    container = MinioContainer()
    with container as minio:
        minio_url = f"http://{minio.get_container_host_ip()}:{minio.get_exposed_port(9000)}"
        logger.info(
            "MinIO container started at %s",
            minio_url
        )
        yield minio


@pytest.fixture(scope='session')
# pylint: disable=R0914, R0915:
async def service_container(
        mongo_container: MongoDbContainer,
        minio_container: MinioContainer
) -> AsyncGenerator[str, None]:
    """Builds and runs the FastAPI service Docker container
    for integration tests.

    This fixture builds a Docker image from the project's Dockerfile,
    sets up environment variables for the service to connect to the
    mock MongoDB and Minio containers, and then starts the service
    container. It waits for the service to become ready (either by
    detecting a startup log message or by a successful health check)
    before yielding the base URL of the running service. After the
    tests using this fixture are finished, the service container is
    automatically stopped.

    Yields:
        str: The base URL (http://host:port) where the service
        is accessible.
    """
    logger.info(
        "Building image '%s' from Dockerfile at '%s'",
        TEST_IMAGE_NAME,
        PROJECT_ROOT
    )

    # Build the image first
    import subprocess  # pylint: disable=C0415
    try:
        result = subprocess.run(
            ['docker', 'build', '-t', TEST_IMAGE_NAME, '.'],
            cwd=str(PROJECT_ROOT),
            check=True,
            capture_output=True,
            text=True
        )
        logger.info('Docker image built successfully')
        logger.debug(
            "Build output: {%s}",
            result.stdout
        )
    except subprocess.CalledProcessError as err:
        logger.error(
            "Failed to build Docker image: %s",
            err
        )
        raise

    # Set Environment Variables
    test_env = {
        'API_VERSION': 'v1',
        'NAME': 'test_app',
        'DESCRIPTION': 'REST API for Pictures',
        'VERSION': '1.0.0',
        'LOG_LEVEL': 'DEBUG',
        'FILE_STORAGE_PROVIDER': 'minio',
        'SWAGGER_ENABLED': 'False',
        'MINIO_ENDPOINT': f"http://{minio_container.get_container_host_ip()}"
                          f":{minio_container.get_exposed_port(9000)}",
        'MINIO_ACCESS_KEY': 'test_access_key',
        'MINIO_SECRET_KEY': 'test_secret_key',
        'MINIO_USE_SSL': 'False',
        'MONGO_URI': f"mongodb://{mongo_container.get_container_host_ip()}"
                     f":{mongo_container.get_exposed_port(27017)}/testdb",
        'MONGO_DB_NAME': 'testdb',
        'MONGO_COLLECTION_NAME': 'test_collection',
    }

    # Create and configure the container
    container = DockerContainer(image=TEST_IMAGE_NAME)
    container.with_exposed_ports(SERVICE_PORT)

    # Apply environment variables
    for key, value in test_env.items():
        container = container.with_env(key, str(value))

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
                'Application startup complete.',
                timeout=120
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
                'Attempting readiness check via /api/health endpoint...'
            )
            max_wait = 120
            start_wait = time.time()
            ready = False

            async with httpx.AsyncClient() as client:
                while time.time() - start_wait < max_wait:
                    try:
                        # Ensure the health check URL includes the protocol
                        health_url = join_urls(
                            base_url, HEALTH_PATH
                        )
                        logger.debug(
                            "Attempting health check at: %s",
                            health_url
                        )
                        response = await client.get(health_url, timeout=5)
                        # pylint: disable=W1404
                        if response.status_code == 200 and response.json().get(
                                ' '"status"
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
                        # Log container logs for debugging
                        logs = running_container.get_logs()[
                            0].decode().strip() if \
                            running_container.get_logs()[0] else ""
                        logs_stderr = running_container.get_logs()[
                            1].decode().strip() if \
                            running_container.get_logs()[1] else ""
                        logger.debug(
                            "Container logs at time of failure:\nSTDOUT:\n%s\nSTDERR:\n%s",
                            logs,
                            logs_stderr
                        )
                    await asyncio.sleep(2)

            if not ready:
                # Dump logs if readiness check fails
                logs = running_container.get_logs()[0].decode().strip() if \
                    running_container.get_logs()[0] else ""
                logs_stderr = running_container.get_logs()[
                    1].decode().strip() if running_container.get_logs()[
                    1] else ''
                logger.error(
                    "Service readiness check failed after %ss.\nSTDOUT:\n%s\nSTDERR:\n%s",
                    max_wait,
                    logs,
                    logs_stderr
                )

                # Try to get more information about the container state
                try:
                    container_info = subprocess.run(
                        ['docker', 'inspect',
                         running_container.get_wrapped_container().id],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    logger.error(
                        "Container state:\n%s",
                        container_info.stdout
                    )
                except subprocess.CalledProcessError as err:
                    logger.error(
                        "Failed to get container info: %s",
                        err.stderr
                    )

                pytest.fail(
                    "Service did not become ready at %s/%s",
                    base_url,
                    HEALTH_PATH
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
            home_url = join_urls(base_url, '')
            logger.info(
                "Testing home endpoint: %s",
                home_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(home_url)

                assert response.status_code == HTTP_200_OK
                # The home endpoint might return JSON instead of HTML
                assert response.headers["content-type"] in [
                    'text/html; charset=utf-8', 'application/json'
                ]

                logger.debug(
                    "Home endpoint response: %s",
                    response.text
                )

                if response.headers['Content-Type'] == 'application/json':
                    data = response.json()
                    assert isinstance(data, dict)
                    assert 'message' in data
                    assert isinstance(data['message'], str)
                else:
                    assert '<html' in response.text.lower()
                    assert '</html>' in response.text.lower()
            break

    @pytest.mark.asyncio
    async def test_root_endpoint(
            self,
            service_container: AsyncGenerator[str, None]
    ):
        """It should test the /api endpoint for a
        successful response."""
        async for base_url in service_container:
            root_url = join_urls(base_url, ROOT_PATH)
            logger.info(
                "Testing root endpoint: %s",
                root_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(root_url)

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
            health_url = join_urls(base_url, HEALTH_PATH)
            logger.info(
                "Testing health endpoint: %s",
                health_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(health_url)

                assert response.status_code == HTTP_200_OK
                assert response.headers["Content-Type"] == 'application/json'
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
            info_url = join_urls(base_url, INFO_PATH)
            logger.info(
                "Testing info endpoint: %s",
                info_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(info_url)

                assert response.status_code == HTTP_200_OK
                assert response.headers["Content-Type"] == 'application/json'

                data = response.json()
                assert isinstance(data, dict)

                assert data.get('name') == app_config.name
                assert data.get('version') == app_config.version
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
            health_url = join_urls(base_url, HEALTH_PATH)
            logger.info(
                "Testing service headers: %s",
                health_url
            )

            async with httpx.AsyncClient() as client:
                response = await client.get(health_url)

                # Check for security headers
                assert 'X-Content-Type-Options' in response.headers
                assert 'X-Frame-Options' in response.headers
                assert 'X-XSS-Protection' in response.headers
            break
