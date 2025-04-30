"""
Picture Service.

This module provides the PictureService class, which encapsulates the business
logic for handling Picture operations.
"""
from __future__ import annotations

import logging
from typing import Optional

from cba_core_lib.storage.errors import FileStorageError
from cba_core_lib.storage.schemas import FileUploadData, SimpleFileData
from cba_core_lib.storage.services import FileStorageService
from service.errors import PictureUploadError, InvalidInputError
from service.schemas import UploadResponseDTO

logger = logging.getLogger(__name__)


class PictureService:
    """Encapsulates the business logic for handling Picture operations, including
    uploading to storage and managing metadata.
    """

    def __init__(
            self,
            file_storage_service: FileStorageService
    ) -> None:
        """Initializes the PictureService.

        Args:
            file_storage_service: Service for interacting with file storage (e.g., S3, MinIO).
        """
        if not file_storage_service:
            error_message = 'FileStorageService dependency is required.'
            logger.error(error_message)
            raise ValueError(error_message)

        self.file_storage_service = file_storage_service
        logger.info(
            "PictureService initialized with storage: %s",
            type(file_storage_service).__name__
        )

    async def upload_file(
            self,
            file_content: bytes,
            original_filename: Optional[str],
            content_type: Optional[str],
            target_bucket: Optional[str] = None
    ) -> UploadResponseDTO:
        """Coordinates file upload to storage, metadata extraction/saving,
        and returns upload details.

        Args:
            file_content: The raw bytes of the file.
            original_filename: The original name of the file.
            content_type: The MIME type of the file.
            target_bucket: Optional identifier for the user performing the upload.

        Returns:
            UploadResponseDTO: Details about the successful upload.

        Raises:
            InvalidInputError: If essential input like file content or filename is missing/invalid.
            PictureUploadError: If the upload to the storage service fails.
            MetadataError: If saving metadata fails.
        """
        logger.info(
            "Processing upload for file: %s to bucket: %s",
            original_filename, target_bucket
        )

        # 1. Validate Input
        if not file_content:
            raise InvalidInputError('Cannot upload an empty file.')
        if not original_filename:
            # Decide policy: generate a name or require it
            raise InvalidInputError(
                'Original filename is required for upload.')
        if not target_bucket:
            raise InvalidInputError('Target bucket must be specified.')

        file_data: FileUploadData = SimpleFileData(
            content_bytes=file_content,
            size=len(file_content),
            filename=original_filename,
            content_type=content_type
        )

        # 2. Upload using the storage service
        try:
            object_name, etag, file_size = await self.file_storage_service.upload_file(
                file_data=file_data,
                bucket_name=target_bucket
            )
            logger.info(
                "File uploaded via %s to %s/%s. Size: %d, ETag: %s",
                type(self.file_storage_service).__name__,
                target_bucket,
                object_name,
                file_size,
                etag
            )
        except FileStorageError as err:
            error_message = f"Storage service failed during upload: {err}"
            logger.error(error_message, exc_info=True)
            raise PictureUploadError(
                error_message,
                original_exception=err
            ) from err
        except ValueError as err:
            error_message = f"Invalid file provided for upload: {err}"
            logger.error(error_message)
            raise InvalidInputError(
                error_message,
                original_exception=err
            ) from err
        except Exception as err:  # pylint: disable=W0703
            error_message = f"Unexpected error during storage upload step: {err}"
            logger.error(error_message, exc_info=True)
            raise PictureUploadError(
                error_message,
                original_exception=err
            ) from err

        # 3. Prepare Metadata

        # 4. Save Metadata to MongoDB

        # 5. Get File URL from the storage service
        try:
            file_url = self.file_storage_service.get_file_url(
                target_bucket,
                object_name
            )
            logger.debug("Retrieved file URL: %s", file_url)
        except FileStorageError as err:
            error_message = f"Failed to get file URL from storage service {err}"
            logger.error(error_message, exc_info=True)
            raise PictureUploadError(
                error_message,
                original_exception=err
            ) from err
        except Exception as err:  # pylint: disable=W0703
            error_message = f"Unexpected error getting file URL: {err}"
            logger.error(error_message, exc_info=True)
            raise PictureUploadError(
                error_message,
                original_exception=err
            ) from err

        # 6. Return Success Response
        return UploadResponseDTO(
            original_filename=original_filename,
            object_name=object_name,
            file_url=file_url,
            size=file_size,
            etag=etag
        )
