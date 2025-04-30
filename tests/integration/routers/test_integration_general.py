"""
General Routers Integration Test Suite.

Test cases can be run with the following:
  pytest -v --with-integration --log-cli-level=DEBUG tests/integration
"""
import logging
from typing import AsyncGenerator

import httpx
import pytest
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from service import app_config
from service.routers.general import HEALTH_PATH, INFO_PATH, ROOT_PATH
from tests import join_urls

logger = logging.getLogger(__name__)


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
                assert response.headers['content-type'] in [
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
