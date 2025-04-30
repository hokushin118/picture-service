"""
Picture Routers Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
from io import BytesIO
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI, UploadFile
from fastapi.testclient import TestClient
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from service.dependencies import get_picture_service
from service.routers.pictures import (
    picture_router,
    PICTURES_PATH_V1
)
from service.schemas import UploadResponseDTO
from service.services import PictureService


############################################################
# FIXTURES
############################################################
@pytest.fixture
def test_app(mock_picture_service: AsyncMock) -> FastAPI:
    """Creates a test FastAPI application with the picture router and
    overridden dependencies.

    This fixture sets up a FastAPI app instance specifically for testing the
    picture_router.It overrides the 'get_picture_service' dependency to use a
    mock PictureService, allowing for isolated testing of the router's
    functionality without relying on the actual service implementation.

    Args:
        mock_picture_service: An AsyncMock instance of the PictureService, used
        to replace the actual service in the application's dependency
        injection.

    Returns:
        FastAPI: A configured FastAPI application instance ready for testing.
    """
    app = FastAPI()
    app.include_router(picture_router)
    app.dependency_overrides[
        get_picture_service
    ] = lambda: mock_picture_service
    return app


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    """Creates a TestClient instance for interacting with the FastAPI test
    application.

    This fixture depends on the 'test_app' fixture to obtain the FastAPI
    application instance. It then initializes a TestClient with this
    application, providing a convenient way to send requests to the
    application within tests.

    Args:
        test_app: The FastAPI application instance created by the 'test_app'
        fixture.

    Returns:
        TestClient: A TestClient instance configured to communicate with the
        test application.
    """
    return TestClient(test_app)


@pytest.fixture
def mock_picture_service() -> AsyncMock:
    """Creates an AsyncMock instance for the PictureService.

    This fixture generates an AsyncMock object that mimics the PictureService
    class. This mock is useful for isolating the testing of components that
    depend on the PictureService, such as routers or other services,
    by replacing the actual service with a controllable substitute.

    Returns:
        AsyncMock: An AsyncMock instance that can be used to simulate a
        PictureService.
    """
    return AsyncMock(spec=PictureService)


def create_test_file(
        filename: str,
        content: bytes,
        content_type: str
) -> UploadFile:
    """Creates a test UploadFile object with a simulated content type.

    This utility function creates an UploadFile object for use in tests.
    It takes the filename, content, and content type as arguments and
    returns a configured UploadFile instance.  The key addition is the
    inclusion of a 'headers' parameter to simulate the content type being
    sent as part of the file upload, which is important for more realistic
    testing scenarios.

    Args:
        filename: The name of the file.
        content: The byte content of the file.
        content_type: The MIME type of the file.

    Returns:
        UploadFile: An UploadFile object with the specified filename, content,
            and content type headers.
    """
    headers = {'content-type': content_type}
    return UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers=headers
    )


class TestFileUpload:
    """Tests for the file upload endpoint."""

    @pytest.mark.asyncio
    async def test_upload_success(
            self,
            test_client: TestClient,
            mock_picture_service: AsyncMock
    ):
        """It should test a successful file upload."""
        # Create a test file
        test_file = create_test_file(
            filename='test_file.txt',
            content=b"This is a test file.",
            content_type='text/plain'
        )
        # Configure the mock service to return a successful result
        mock_picture_service.upload_file.return_value = UploadResponseDTO()

        response = test_client.post(
            PICTURES_PATH_V1,
            files={'file': ('test_file.txt', test_file.file, 'text/plain')}
        )

        assert response.status_code == HTTP_201_CREATED
        mock_picture_service.upload_file.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_file_read_error(
            self,
            test_client: TestClient,
            mock_picture_service: AsyncMock
    ):
        """It should raise a PictureError when there's an error
        reading the file."""
        # Create a test file
        test_file = create_test_file(
            filename='error_file.txt',
            content=b"This is a test file.",
            content_type="text/plain"
        )
        # Mock file.read() to raise an exception
        with patch.object(test_file.file, 'read') as mock_read:
            mock_read.side_effect = Exception('Failed to read file')
            response = test_client.post(
                PICTURES_PATH_V1,
                files={
                    'file': ('error_file.txt', test_file.file, 'text/plain')
                }
            )
            assert response.status_code == HTTP_400_BAD_REQUEST
            data = response.json()
            assert 'detail' in data
            assert 'There was an error parsing the body' in data['detail']
            mock_picture_service.upload_file.assert_not_called()
