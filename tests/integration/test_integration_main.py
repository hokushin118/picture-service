"""
Application Integration Test Suite.

Test cases can be run with the following:
  pytest -v --with-integration tests/integration
"""
import pytest
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK

from service.configs import AppConfig
from service.main import app


############################################################
# INTEGRATION TESTS SCENARIOS
############################################################
@pytest.mark.integration
class TestFastAPIIntegration:
    """Integration tests for the FastAPI application."""

    @pytest.fixture
    def test_app(self):
        """Fixture to create a test FastAPI client."""
        return TestClient(app)

    def test_create_app_title(self):
        """It should verify the app's title."""
        assert app.title == AppConfig().description

    def test_create_app_version(self):
        """It should verify the app's version."""
        assert app.version == AppConfig().version

    def test_docs_endpoint(self, test_app):
        """It should verify the /docs endpoint is accessible."""
        response = test_app.get('/docs')
        assert response.status_code == HTTP_200_OK

    def test_redoc_endpoint(self, test_app):
        """It should verify the /redoc endpoint is accessible."""
        response = test_app.get('/redoc')
        assert response.status_code == HTTP_200_OK
