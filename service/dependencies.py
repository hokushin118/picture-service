"""
Dependency injection module.

This module provides functionality to inject dependency injection into the
service.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Annotated

from cba_core_lib.storage.configs import MinioConfig
from cba_core_lib.storage.errors import FileStorageError
from cba_core_lib.storage.services import FileStorageService, MinioService
from fastapi import Depends

from service import app_config
from service.errors import PictureError
from service.services import PictureService

logger = logging.getLogger(__name__)


@lru_cache()  # Cache the service instance for the app lifetime
def get_file_storage_service() -> FileStorageService:
    """Factory function to create and return a file storage service instance.

    This function determines the storage provider from the application
    configuration and returns an instance of the corresponding service
    (e.g., MinioService).  The result is cached for the lifetime of the
    application to ensure only one instance is created.

    Returns:
        An instance of a FileStorageService (e.g., MinioService).

    Raises:
        ValueError: If the configured file storage provider is not supported.
        RuntimeError: If there is an error initializing the storage service.
    """
    storage_provider = app_config.file_storage_provider
    logger.info(
        "Creating storage service based on provider: %s",
        storage_provider
    )
    try:
        if storage_provider == 'minio':
            minio_config = MinioConfig()
            return MinioService(minio_config)

        error_message = f"Unsupported file storage provider:{storage_provider}"
        logger.error(error_message)
        raise ValueError(error_message)
    except (
            FileStorageError,
            ValueError,
            Exception
    ) as err:
        error_message = (
            f"Failed to initialize storage service provider {storage_provider}': {err}"
        )
        # pylint: disable=R0801
        logger.error(error_message, exc_info=True)
        raise PictureError(
            error_message,
            original_exception=err
        ) from err


def get_picture_service(
        file_storage_service: Annotated[
            FileStorageService, Depends(get_file_storage_service)
        ]
) -> PictureService:
    """Provides an instance of the PictureService with its dependencies
    injected.

    This factory function creates a PictureService instance, injecting the
    required FileStorageService dependency. This is used by FastAPI's
    dependency injection system.

    Args:
        file_storage_service:  An instance of FileStorageService, which is
            itself obtained via FastAPI's dependency injection.  This service
            handles the actual interaction with the file storage system
            (e.g., MinIO, AWS).

    Returns:
        An instance of PictureService, ready to be used for handling picture
        uploads and related operations.
    """
    logger.debug('Creating PictureService instance...')
    return PictureService(
        file_storage_service=file_storage_service
    )
