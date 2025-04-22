"""
Configs Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
from datetime import timezone, datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient

from service import NAME, VERSION
from service.routes import HEALTH_PATH, INFO_PATH
from service.schemas import HealthCheckDTO, InfoDTO


class TestHealthEndpoint:
    """The /health Endpoint Tests."""

    def test_health_endpoint(
            self,
            test_client: TestClient
    ):
        """It should test the /health endpoint to ensure it returns the
        correct status and response."""
        response = test_client.get(HEALTH_PATH)
        assert response.status_code == 200
        assert response.json() == {'status': 'UP'}
        # Optionally, validate against the schema
        health_check_dto = HealthCheckDTO(**response.json())
        assert health_check_dto.status == 'UP'


class TestInfoEndpoint:
    """The /info Endpoint Tests."""

    def test_info_endpoint(
            self,
            test_client: TestClient,
            test_app: FastAPI
    ):
        """It should test the /info endpoint to ensure it returns the
        correct information. This test also verifies the uptime calculation."""
        start_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        test_app.state.start_time = start_time

        response = test_client.get(INFO_PATH)
        assert response.status_code == 200
        info = response.json()

        # Validate the basic structure
        assert 'name' in info
        assert 'version' in info
        assert 'uptime' in info

        # Validate the values
        assert info['name'] == NAME
        assert info['version'] == VERSION

        # Check that uptime is a string and is not "Not yet started"
        assert isinstance(info['uptime'], str)
        assert info['uptime'] != 'Not yet started'

        # Optionally, validate against the schema
        info_dto = InfoDTO(**info)
        assert info_dto.name == NAME
        assert info_dto.version == VERSION
        assert isinstance(info_dto.uptime, str)

    def test_info_endpoint_no_start_time(
            self,
            test_client: TestClient
    ):
        """It should test the /info endpoint when app.state.start_time
        is not set."""
        response = test_client.get(INFO_PATH)
        assert response.status_code == 200
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
        assert response.status_code == 200
        info = response.json()
        assert info['uptime'] == \
               'Error: Invalid start_time format in app state'
