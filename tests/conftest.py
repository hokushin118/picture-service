"""
Unit Test Suite Fixtures.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
import asyncio
import logging
import time
from typing import AsyncGenerator

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.minio import MinioContainer
from testcontainers.mongodb import MongoDbContainer
from service.routers.general import general_router, HEALTH_PATH
from service.routers.pictures import picture_router
from tests import join_urls, ensure_url
from tests import (
    SERVICE_PORT,
    TEST_IMAGE_NAME,
    PROJECT_ROOT
)

logger = logging.getLogger(__name__)


############################################################
# TEST FIXTURES
############################################################
@pytest.fixture
def test_app() -> FastAPI:
    """This fixture creates a test instance of the FastAPI application.
    It's used to ensure that the tests are run in an isolated environment,
    preventing interference with any running application.  The router is
    included to make the application's routers available to the test client.

    Returns:
        FastAPI: An instance of the FastAPI application.
    """
    app = FastAPI()
    app.include_router(general_router)
    app.include_router(picture_router)
    return app


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:  # pylint: disable=W0621
    """This fixture creates a TestClient instance using the FastAPI test
    application created by the `test_app` fixture.  The TestClient is a
    powerful tool for testing FastAPI applications, allowing you to send
    requests to your application without needing to start a server.

    Args:
        test_app (FastAPI):  The FastAPI application instance created by the
            `test_app` fixture.  This is used to initialize the TestClient.

    Returns:
        TestClient: An instance of the FastAPI TestClient.
    """
    return TestClient(test_app)


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
