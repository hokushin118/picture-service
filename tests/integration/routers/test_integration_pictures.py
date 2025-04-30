"""
Picture Routers Integration Test Suite.

Test cases can be run with the following:
  pytest -v --with-integration --log-cli-level=DEBUG tests/integration
"""
import logging
from typing import AsyncGenerator

import httpx
import pytest
from minio import Minio
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from testcontainers.core.container import DockerContainer
from service.routers.pictures import PICTURES_PATH_V1
from tests import join_urls, TEST_CONTENT_TYPE, TEST_BUCKET_NAME

logger = logging.getLogger(__name__)


############################################################
# FIXTURES
############################################################
@pytest.fixture(scope='session')
async def minio_client(
        minio_container: AsyncGenerator[DockerContainer, None]
) -> AsyncGenerator[Minio, None]:
    """Creates a MinIO client configured to connect to the test container.

    Args:
        minio_container: The running MinIO container.

    Yields:
        Minio: A configured Minio client instance.
    """
    async for container in minio_container:
        client = Minio(
            f"{container.get_container_host_ip()}:{container.get_exposed_port(9000)}",
            access_key='minioadmin',
            secret_key='minioadmin',
            secure=False
        )
        yield client


############################################################
# INTEGRATION TESTS SCENARIOS
############################################################
@pytest.mark.integration
class TestPictureEndpointIntegration:
    """The Picture Endpoints Integration Tests."""

    @pytest.mark.asyncio
    async def test_upload_success(
            self,
            service_container: AsyncGenerator[str, None],
            minio_client: Minio
    ):
        """It should test successful file upload."""
        async for base_url in service_container:
            upload_url = join_urls(base_url, PICTURES_PATH_V1)
            logger.info(
                "Testing upload endpoint: %s",
                upload_url
            )

            # Create a test file
            test_content = b"This is a test file for integration testing."
            test_file = (
                'test_integration.txt',
                test_content,
                TEST_CONTENT_TYPE
            )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    upload_url,
                    files={'file': test_file}
                )

                assert response.status_code == HTTP_201_CREATED
                assert response.headers['Content-Type'] == 'application/json'

                data = response.json()
                assert isinstance(data, dict)
                assert 'object_name' in data
                assert 'url' in data
                assert 'content_type' in data
                assert 'size' in data
                assert data['size'] == len(test_content)

                # Verify the file exists in MinIO
                assert minio_client.bucket_exists(TEST_BUCKET_NAME)
                assert minio_client.stat_object(
                    TEST_BUCKET_NAME,
                    data['object_name']
                )
            break

    @pytest.mark.asyncio
    async def test_upload_empty_file(
            self,
            service_container: AsyncGenerator[str, None]
    ):
        """It should test uploading an empty file."""
        async for base_url in service_container:
            upload_url = join_urls(base_url, PICTURES_PATH_V1)
            logger.info(
                "Testing empty file upload: %s",
                upload_url
            )

            # Create an empty test file
            test_file = (
                'empty_file.txt',
                b"",
                TEST_CONTENT_TYPE
            )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    upload_url,
                    files={'file': test_file}
                )

                assert response.status_code == HTTP_400_BAD_REQUEST
                assert response.headers['Content-Type'] == 'application/json'

                data = response.json()
                assert 'detail' in data
                assert 'Cannot upload an empty file' in data['detail']
            break

    @pytest.mark.asyncio
    async def test_upload_large_file(
            self,
            service_container: AsyncGenerator[str, None],
            minio_client: Minio
    ):
        """It should test uploading a large file."""
        async for base_url in service_container:
            upload_url = join_urls(base_url, PICTURES_PATH_V1)
            logger.info(
                "Testing large file upload: %s",
                upload_url
            )

            # Create a large test file (5MB)
            large_content = b"x" * (5 * 1024 * 1024)
            test_file = (
                'large_file.txt',
                large_content,
                TEST_CONTENT_TYPE
            )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    upload_url,
                    files={'file': test_file}
                )

                assert response.status_code == HTTP_201_CREATED
                assert response.headers['Content-Type'] == 'application/json'

                data = response.json()
                assert isinstance(data, dict)
                assert 'size' in data
                assert data['size'] == len(large_content)

                # Verify the file exists in MinIO
                stat = minio_client.stat_object(
                    TEST_BUCKET_NAME,
                    data['object_name']
                )
                assert stat.size == len(large_content)
            break

    @pytest.mark.asyncio
    async def test_upload_invalid_content_type(
            self,
            service_container: AsyncGenerator[str, None],
            minio_client: Minio
    ):
        """It should test uploading a file with an invalid content type."""
        async for base_url in service_container:
            upload_url = join_urls(base_url, PICTURES_PATH_V1)
            logger.info(
                "Testing invalid content type upload: %s",
                upload_url
            )

            # Create a test file with invalid content type
            test_file = (
                'test.xyz',
                b"Test content",
                'application/invalid'
            )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    upload_url,
                    files={'file': test_file}
                )

                assert response.status_code == HTTP_201_CREATED
                assert response.headers['Content-Type'] == 'application/json'

                data = response.json()
                assert isinstance(data, dict)
                assert 'content_type' in data
                assert data['content_type'] == 'application/invalid'

                # Verify the file exists in MinIO with the specified content type
                stat = minio_client.stat_object(
                    TEST_BUCKET_NAME,
                    data['object_name']
                )
                assert stat.content_type == 'application/invalid'
            break

    @pytest.mark.asyncio
    async def test_upload_special_characters_filename(
            self,
            service_container: AsyncGenerator[str, None],
            minio_client: Minio
    ):
        """It should test uploading a file with special characters in
        the filename."""
        async for base_url in service_container:
            upload_url = join_urls(base_url, PICTURES_PATH_V1)
            logger.info(
                "Testing special characters filename upload: %s",
                upload_url
            )

            # Create a test file with special characters in name
            test_file = (
                'test@#$%^&*.txt',
                b"Test content",
                TEST_CONTENT_TYPE
            )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    upload_url,
                    files={'file': test_file}
                )

                assert response.status_code == HTTP_201_CREATED
                assert response.headers['Content-Type'] == 'application/json'

                data = response.json()
                assert isinstance(data, dict)
                assert 'object_name' in data

                # Verify the file exists in MinIO
                assert minio_client.stat_object(
                    TEST_BUCKET_NAME,
                    data['object_name']
                )
            break

    @pytest.mark.asyncio
    async def test_upload_duplicate_filename(
            self,
            service_container: AsyncGenerator[str, None],
            minio_client: Minio
    ):
        """It should test uploading a file with a duplicate filename."""
        async for base_url in service_container:
            upload_url = join_urls(base_url, PICTURES_PATH_V1)
            logger.info(
                "Testing duplicate filename upload: %s",
                upload_url
            )

            # Create and upload first file
            test_file = (
                'duplicate.txt',
                b"First file content",
                TEST_CONTENT_TYPE
            )

            async with httpx.AsyncClient() as client:
                # Upload first file
                response1 = await client.post(
                    upload_url,
                    files={'file': test_file}
                )
                assert response1.status_code == HTTP_201_CREATED
                data1 = response1.json()
                assert 'object_name' in data1

                # Upload second file with same name
                response2 = await client.post(
                    upload_url,
                    files={'file': test_file}
                )
                assert response2.status_code == HTTP_201_CREATED
                data2 = response2.json()
                assert 'object_name' in data2

                # Verify both files exist in MinIO with different object names
                assert minio_client.stat_object(
                    TEST_BUCKET_NAME,
                    data1['object_name']
                )
                assert minio_client.stat_object(
                    TEST_BUCKET_NAME,
                    data2['object_name']
                )
                assert data1['object_name'] != data2['object_name']
            break

    @pytest.mark.asyncio
    async def test_upload_very_large_file(
            self,
            service_container: AsyncGenerator[str, None],
            minio_client: AsyncGenerator[Minio, None]
    ):
        """It should test uploading a very large file (10MB)."""
        async for base_url in service_container:
            async for client in minio_client:
                upload_url = join_urls(base_url, PICTURES_PATH_V1)
                logger.info(
                    "Testing very large file upload: %s",
                    upload_url
                )

                # Create a very large test file (10MB)
                large_content = b"x" * (10 * 1024 * 1024)
                test_file = (
                    'very_large_file.txt',
                    large_content,
                    TEST_CONTENT_TYPE
                )

                async with httpx.AsyncClient() as http_client:
                    response = await http_client.post(
                        upload_url,
                        files={'file': test_file}
                    )

                    assert response.status_code == HTTP_201_CREATED
                    assert response.headers[
                               'Content-Type'
                           ] == 'application/json'
                    data = response.json()
                    assert isinstance(data, dict)
                    assert 'size' in data
                    assert data['size'] == len(large_content)

                    # Verify the file exists in MinIO
                    stat = client.stat_object(
                        TEST_BUCKET_NAME,
                        data['object_name']
                    )
                    assert stat.size == len(large_content)
                break
