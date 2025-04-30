"""
Schemas for Picture microservice.

All schemas are stored in this module.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, HttpUrl
from service import app_config

MIN_LENGTH = 1


######################################################################
# VALIDATION METHODS
######################################################################
def check_not_whitespace_only(
        value: str
) -> str:
    """Ensure the string is not composed solely of whitespace.

    This function checks if the input string, after removing leading and trailing
    whitespace, is empty. If the stripped string is empty, it raises a
    ValueError.

    Args:
        value (str): The string to check.

    Returns:
        str: The original string if it is not composed solely of whitespace.

    Raises:
        ValueError: If the string consists only of whitespace characters.
    """
    if isinstance(value, str):
        if not value or value.isspace():
            raise ValueError(
                'Field cannot consist only of whitespace.'
            )
    return value


######################################################################
# SCHEMAS
######################################################################
class IndexDTO(BaseModel):
    """Represents the response body for a root endpoint.

    Indicates the welcome message of the service.

    Attributes:
        message (str): The welcome message for the API.
    """
    message: str = Field(
        ...,
        min_length=MIN_LENGTH,
        description="The welcome message of the service (e.g., 'Welcome').",
        examples=['Welcome to the Picture API!']
    )

    @field_validator('message')
    # pylint: disable=no-self-argument
    def check_message_not_whitespace_only(
            cls,
            value: str
    ) -> str:
        """Validates that the message string is not composed solely
        of whitespace.

        This validator is applied to the 'message' field of the
        IndexDTO model. It uses the `check_not_whitespace_only`
        function to perform the validation.

        Args:
            cls: The class of the model (IndexDTO).
            This is automatically passed by Pydantic and is conventionally
            named `cls`.
            value (str): The value of the 'message' field to be validated.

        Returns:
            str: The validated message string.

        Raises:
            ValueError: If the message string contains only whitespace
            characters.
        """
        return check_not_whitespace_only(value)


class HealthCheckDTO(BaseModel):
    """Represents the response body for a health check endpoint.

    Indicates the operational status of the service.

    Attributes:
        status (str): The operational status of the service
         (e.g., 'UP'). Describes whether the service considers itself
         operational.
    """
    status: str = Field(
        ...,
        min_length=MIN_LENGTH,
        description="The operational status of the service (e.g., 'UP'').",
        examples=['UP']
    )

    @field_validator('status')
    # pylint: disable=no-self-argument
    def check_status_not_whitespace_only(
            cls,
            value: str
    ) -> str:
        """Validates that the status string is not composed solely
        of whitespace.

        This validator is applied to the 'status' field of the
        HealthCheckDTO model. It uses the `check_not_whitespace_only`
        function to perform the validation.

        Args:
            cls: The class of the model (HealthCheckDTO).
            This is automatically passed by Pydantic and is conventionally
            named `cls`.
            value (str): The value of the 'status' field to be validated.

        Returns:
            str: The validated status string.

        Raises:
            ValueError: If the status string contains only whitespace
            characters.
        """
        return check_not_whitespace_only(value)


class InfoDTO(BaseModel):
    """Represents the response body for the service information endpoint.

    Provides basic metadata about the running service instance, such as its
    name, deployed version, and how long it has been running.

    Attributes:
        name (str): The configured or registered name of the running service.
        version (str): The current deployed version identifier of the service.
        uptime (str): A human-readable string representation of the duration the
                      service has been continuously running since its last start
                      (e.g., "1 days, 2:03:45.123456", "0:15:32.548123").
    """
    name: str = Field(
        ...,
        min_length=MIN_LENGTH,
        description='The configured name of the running service.',
        examples=[app_config.name]
    )
    version: str = Field(
        ...,
        min_length=MIN_LENGTH,
        description='The current deployed version identifier of the service.',
        examples=[app_config.version]
    )
    uptime: str = Field(
        ...,
        min_length=MIN_LENGTH,
        description='A string representation of the duration the service has been running.',
        examples=['0:15:32.548123', '3 days, 2:05:55.987654']
    )

    @field_validator('name', 'version', mode='before')
    # pylint: disable=no-self-argument
    def check_field_not_whitespace_only(
            cls,
            value: str
    ) -> str:
        """Validates that specific string fields are not None, empty, or
        contain only whitespace.

        Args:
            cls: The class of the model (InfoDTO).
            This is automatically passed by Pydantic and is conventionally
            named `cls`.
            value (str): The value of the field to be validated.

        Returns:
            str: The validated name string.

        Raises:
            ValueError: If the name string contains only whitespace
            characters.
        """
        return check_not_whitespace_only(value)


class UploadResponseDTO(BaseModel):
    """Represents the response body for the file upload endpoint. Provides
    metadata about the uploaded file.
    """
    original_filename: str = Field(
        ...,
        min_length=MIN_LENGTH,
        description='The original filename provided during upload.',
        examples=['vacation_photo.png']
    )
    object_name: str = Field(
        ...,
        min_length=MIN_LENGTH,
        description='The final name (key) of the object stored in the bucket.',
        examples=['user_data/vacation_photo_uuid123.png']
    )
    file_url: HttpUrl = Field(
        ...,
        description='The accessible URL for the uploaded file.',
        examples=[
            'https://my-minio.example.com/pictures/user_data/vacation_photo_uuid123.png']
    )
    size: int = Field(
        ...,
        ge=0,
        description='The size of the uploaded file in bytes.',
        examples=[5242880]  # 5 MB example
    )
    etag: str = Field(
        ...,
        min_length=MIN_LENGTH,
        description='The ETag (Entity Tag) of the uploaded object from storage.',
        examples=['fba9dede5f27731c9771645a39863328']
    )

    @field_validator('original_filename', 'object_name', 'etag', mode='before')
    # pylint: disable=no-self-argument
    def check_field_not_whitespace_only(
            cls,
            value: str
    ) -> str:
        """Validates that specific string fields are not None, empty, or
        contain only whitespace.

        Args:
            cls: The class of the model (UploadResponseDTO).
            This is automatically passed by Pydantic and is conventionally
            named `cls`.
            value (str): The value of the field to be validated.

        Returns:
            str: The validated version string.

        Raises:
            ValueError: If the version string contains only whitespace
            characters.
        """
        return check_not_whitespace_only(value)
