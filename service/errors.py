"""
Custom errors for Picture microservice.

This module defines custom exception classes for the picture service.
"""
from __future__ import annotations

from typing import Optional


class PictureError(Exception):
    """Base exception class for picture-related errors.

    This class serves as the foundation for more specific exceptions
    within the picture service. It provides a consistent interface
    for handling errors associated with picture operations.

    Attributes:
        message: A human-readable error message (string).
        original_exception:  The original exception that caused this error,
            if any (Optional[Exception]).  This allows for exception
            chaining to preserve the full context of the error.
    """

    def __init__(
            self,
            message: str,
            original_exception: Optional[Exception] = None
    ):
        """Initializes a PictureError instance.

        Args:
            message: The error message.
            original_exception: The original exception.
        """
        self.message = message
        self.original_exception = original_exception
        super().__init__(message)


class PictureUploadError(PictureError):
    """Exception raised when an error occurs during the picture upload process.

    This exception is specifically used to indicate problems that arise
    while uploading a picture, such as file reading issues, storage
    service failures, or invalid file data.
    """


class InvalidInputError(PictureError):
    """Exception raised when the input provided by the user is invalid.

    This exception is used to signal that the user has provided data that
    does not meet the required criteria, such as an empty file, incorrect
    data format, or missing required fields.
    """
