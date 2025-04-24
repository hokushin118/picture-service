"""
Configs Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
from datetime import timezone, datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK

from service import app_config
from service.routes import HEALTH_PATH, INFO_PATH, ROOT_PATH
from service.schemas import HealthCheckDTO, InfoDTO, IndexDTO


class TestIndexEndpoint:
    """The /api Endpoint Tests."""

    def test_index_endpoint(
            self,
            test_client: TestClient
    ):
        """It should test the /api endpoint to ensure it returns the
        correct status and response."""
        response = test_client.get(ROOT_PATH)
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'Welcome to the Picture API!'}
        # Validate against the schema
        index_dto = IndexDTO(**response.json())
        assert index_dto.message == 'Welcome to the Picture API!'


class TestHealthEndpoint:
    """The /api/health Endpoint Tests."""

    def test_health_endpoint(
            self,
            test_client: TestClient
    ):
        """It should test the /api/health endpoint to ensure it returns the
        correct status and response."""
        response = test_client.get(HEALTH_PATH)
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'status': 'UP'}
        # Validate against the schema
        health_check_dto = HealthCheckDTO(**response.json())
        assert health_check_dto.status == 'UP'


class TestInfoEndpoint:
    """The /api/info Endpoint Tests."""

    def test_info_endpoint(
            self,
            test_client: TestClient,
            test_app: FastAPI
    ):
        """It should test the /api/info endpoint to ensure it returns the
        correct information. This test also verifies the uptime calculation."""
        start_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        test_app.state.start_time = start_time

        response = test_client.get(INFO_PATH)
        assert response.status_code == HTTP_200_OK
        info = response.json()

        # Validate the basic structure
        assert 'name' in info
        assert 'version' in info
        assert 'uptime' in info

        # Validate the values
        assert info['name'] == app_config.name
        assert info['version'] == app_config.version

        # Check that uptime is a string and is not "Not yet started"
        assert isinstance(info['uptime'], str)
        assert info['uptime'] != 'Not yet started'

        # Validate against the schema
        info_dto = InfoDTO(**info)
        assert info_dto.name == app_config.name
        assert info_dto.version == app_config.version
        assert isinstance(info_dto.uptime, str)

    def test_info_endpoint_no_start_time(
            self,
            test_client: TestClient
    ):
        """It should test the /info endpoint when app.state.start_time
        is not set."""
        response = test_client.get(INFO_PATH)
        assert response.status_code == HTTP_200_OK
        info = response.json()
        assert info['uptime'] == 'Not yet started'

    def test_info_endpoint_invalid_start_time(
            self,
            test_client: TestClient,
            test_app: FastAPI
    ):
        """It should test the /info endpoint when app.state.start_time is
        set to an invalid value."""
        test_app.state.start_time = 'invalid'
        response = test_client.get(INFO_PATH)
        assert response.status_code == HTTP_200_OK
        info = response.json()
        assert info['uptime'] == \
               'Error: Invalid start_time format in app state'
