"""
Unit Test Suite Fixtures.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from service.routes import router


############################################################
# UNIT TEST FIXTURES
############################################################
@pytest.fixture
def test_app() -> FastAPI:
    """This fixture creates a test instance of the FastAPI application.
    It's used to ensure that the tests are run in an isolated environment,
    preventing interference with any running application.  The router is
    included to make the application's routes available to the test client.

    Returns:
        FastAPI: An instance of the FastAPI application.
    """
    app = FastAPI()
    app.include_router(router)
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
