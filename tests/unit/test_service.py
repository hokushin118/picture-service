"""
PictureService Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
from unittest.mock import AsyncMock, MagicMock

import pytest
from cba_core_lib.storage.errors import FileStorageError
from cba_core_lib.storage.services import FileStorageService
from service.errors import PictureUploadError, InvalidInputError
from service.schemas import UploadResponseDTO
from service.services import PictureService
from tests import (
    TEST_OBJECT_NAME,
    TEST_ETAG,
    TEST_FILE_SIZE,
    TEST_URL,
    TEST_CONTENT,
    TEST_CONTENT_TYPE,
    TEST_BUCKET_NAME
)


############################################################
# TEST FIXTURES
############################################################
@pytest.fixture
def mock_storage_service():
    """Creates a mock FileStorageService.

    This fixture provides an AsyncMock instance that simulates the behavior of a
    FileStorageService.  It is used to isolate the PictureService from actual
    file storage operations during testing.  The mock is pre-configured to
    return specific values for file uploads and URL retrieval.

    Returns:
        AsyncMock: A mock object simulating FileStorageService.
    """
    service = AsyncMock(spec=FileStorageService)
    service.upload_file = AsyncMock(
        return_value=(
            TEST_OBJECT_NAME,
            TEST_ETAG,
            TEST_FILE_SIZE
        )
    )
    service.get_file_url = MagicMock(return_value=TEST_URL)
    return service


@pytest.fixture
def picture_service(mock_storage_service):
    """Creates a PictureService instance with a mock storage service.

    This fixture initializes a PictureService with the mock FileStorageService
    provided by the `mock_storage_service` fixture.  This ensures that
    PictureService is tested in isolation, without relying on a real
    file storage backend.

    Args:
        mock_storage_service:  The mock FileStorageService instance to use.

    Returns:
        PictureService: An instance of PictureService configured with the mock
        storage service.
    """
    return PictureService(mock_storage_service)


############################################################
# TESTS SCENARIOS
############################################################
class TestPictureService:
    """The PictureService Class Tests."""

    @pytest.mark.asyncio
    async def test_init_without_storage_service(self):
        """It should raise ValueError when initialized without a
        storage service."""
        with pytest.raises(ValueError) as exc_info:
            PictureService(None)
        assert 'FileStorageService dependency is required' in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_upload_file_success(
            self,
            picture_service,
            mock_storage_service
    ):
        """It should return UploadResponseDTO on successful file upload."""
        result = await picture_service.upload_file(
            file_content=TEST_CONTENT,
            original_filename=TEST_OBJECT_NAME,
            content_type=TEST_CONTENT_TYPE,
            target_bucket=TEST_BUCKET_NAME
        )

        assert isinstance(result, UploadResponseDTO)
        mock_storage_service.upload_file.assert_called_once()
        mock_storage_service.get_file_url.assert_called_once_with(
            TEST_BUCKET_NAME,
            TEST_OBJECT_NAME
        )

    @pytest.mark.asyncio
    async def test_upload_file_empty_content(
            self,
            picture_service
    ):
        """It should raise InvalidInputError when uploading an empty file."""
        with pytest.raises(InvalidInputError) as exc_info:
            await picture_service.upload_file(
                file_content=b"",
                original_filename=TEST_OBJECT_NAME,
                content_type=TEST_CONTENT_TYPE,
                target_bucket=TEST_BUCKET_NAME
            )
        assert 'Cannot upload an empty file' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_upload_file_missing_filename(
            self,
            picture_service
    ):
        """It should raise InvalidInputError when uploading without
         a filename."""
        with pytest.raises(InvalidInputError) as exc_info:
            await picture_service.upload_file(
                file_content=TEST_CONTENT,
                original_filename=None,
                content_type=TEST_CONTENT_TYPE,
                target_bucket=TEST_BUCKET_NAME
            )
        assert 'Original filename is required' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_upload_file_missing_bucket(
            self,
            picture_service
    ):
        """It should raise InvalidInputError when uploading without
        a bucket."""
        with pytest.raises(InvalidInputError) as exc_info:
            await picture_service.upload_file(
                file_content=TEST_CONTENT,
                original_filename=TEST_OBJECT_NAME,
                content_type=TEST_CONTENT_TYPE,
                target_bucket=None
            )
        assert 'Target bucket must be specified' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_upload_file_storage_error(
            self,
            picture_service,
            mock_storage_service
    ):
        """It should raise PictureUploadError for storage service errors."""
        mock_storage_service.upload_file.side_effect = FileStorageError(
            'Storage error'
        )

        with pytest.raises(PictureUploadError) as exc_info:
            await picture_service.upload_file(
                file_content=TEST_CONTENT,
                original_filename=TEST_OBJECT_NAME,
                content_type=TEST_CONTENT_TYPE,
                target_bucket=TEST_BUCKET_NAME
            )
        assert 'Storage service failed during upload' in str(exc_info.value)
        assert isinstance(exc_info.value.original_exception, FileStorageError)

    @pytest.mark.asyncio
    async def test_upload_file_url_error(
            self,
            picture_service,
            mock_storage_service
    ):
        """It should raise PictureUploadError for URL retrieval errors."""
        mock_storage_service.get_file_url.side_effect = FileStorageError(
            'URL error'
        )

        with pytest.raises(PictureUploadError) as exc_info:
            await picture_service.upload_file(
                file_content=TEST_CONTENT,
                original_filename=TEST_OBJECT_NAME,
                content_type=TEST_CONTENT_TYPE,
                target_bucket=TEST_BUCKET_NAME
            )
        assert 'Failed to get file URL from storage service' in str(
            exc_info.value
        )
        assert isinstance(exc_info.value.original_exception, FileStorageError)

    @pytest.mark.asyncio
    async def test_upload_file_unexpected_error(
            self,
            picture_service,
            mock_storage_service
    ):
        """It should raise PictureUploadError for unexpected errors."""
        mock_storage_service.upload_file.side_effect = Exception(
            'Unexpected error'
        )

        with pytest.raises(PictureUploadError) as exc_info:
            await picture_service.upload_file(
                file_content=TEST_CONTENT,
                original_filename=TEST_OBJECT_NAME,
                content_type=TEST_CONTENT_TYPE,
                target_bucket=TEST_BUCKET_NAME
            )
        assert 'Unexpected error during storage upload step' in str(
            exc_info.value
        )
        assert isinstance(exc_info.value.original_exception, Exception)
