"""
Picture API Routers.

This microservice handles the application pictures.
"""
from __future__ import annotations

import logging
from typing import Annotated

from fastapi import (
    APIRouter,
    UploadFile,
    Depends
)
from starlette.status import (
    HTTP_201_CREATED
)

from service.dependencies import get_picture_service
from service.errors import InvalidInputError, PictureError
from service.routers import ROOT_PATH
from service.schemas import UploadResponseDTO
from service.services import PictureService

logger = logging.getLogger(__name__)

PICTURES_PATH_V1 = f"{ROOT_PATH}/v1/pictures"

picture_router = APIRouter(
    prefix='',
    tags=['Picture']
)


############################################################
# FILE UPLOAD
############################################################
@picture_router.post(
    PICTURES_PATH_V1,
    name='pictures:upload',
    response_model=UploadResponseDTO,
    status_code=HTTP_201_CREATED,
    summary='Upload a picture',
    description='Uploads a picture file to the configured storage service.'
                '</br></br>The file is stored in a bucket, and its metadata '
                'is returned.</br></br>Only authenticated users can access '
                'this endpoint.',
    response_description='Uploaded file metadata'
)
async def upload(
        file: UploadFile,
        picture_service: Annotated[PictureService, Depends(
            get_picture_service)
        ],
) -> UploadResponseDTO:
    """Uploads a file to the storage service.

    Args:
        file: The file to upload, provided as a FastAPI UploadFile object.
        picture_service:  The PictureService instance, injected by FastAPI's
            dependency injection system.

    Returns:
        An UploadResponseDTO instance containing metadata about the
        uploaded file.
    """
    filename = file.filename
    logger.info("Received upload request for file: %s", filename)

    try:
        contents = await file.read()
        if not contents:
            error_message = 'Cannot upload an empty file.'
            logger.warning("Upload attempt with empty file: %s", filename)
            raise InvalidInputError(error_message)
    except Exception as err:  # pylint: disable=W0703
        error_message = f"Failed to read uploaded file {filename}: {err}"
        logger.error(error_message, exc_info=True)
        raise PictureError(
            error_message,
            original_exception=err
        ) from err
    finally:
        await file.close()
        logger.debug("Closed file handle for '%s'", filename)

    # The name of the bucket to upload the file to
    uploader_user_id = 'test'

    # Upload a file to the storage
    upload_result = await picture_service.upload_file(
        file_content=contents,
        original_filename=filename,
        content_type=file.content_type,
        target_bucket=uploader_user_id
    )

    return upload_result
