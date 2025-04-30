"""
Custom Errors Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
from service.errors import PictureError, PictureUploadError, InvalidInputError


class TestPictureError:
    """The PictureError Class Tests."""

    def test_picture_error_instantiation(self):
        """It should test that PictureError can be instantiated with
         a message."""
        message = 'A picture error occurred.'
        error = PictureError(message)
        assert error.message == message
        assert error.original_exception is None
        assert str(error) == message

    def test_picture_error_instantiation_with_original_exception(self):
        """It should test that PictureError can be instantiated with an
        original exception."""
        message = 'A picture error occurred.'
        original_exception = ValueError('Original error')
        error = PictureError(message, original_exception)
        assert error.message == message
        assert error.original_exception == original_exception
        assert str(error) == message


class TestPictureUploadError:
    """The PictureUploadError Class Tests."""

    def test_picture_upload_error_instantiation(self):
        """It should test that PictureUploadError can be instantiated
        with a message."""
        message = 'Picture upload failed.'
        error = PictureUploadError(message)
        assert error.message == message
        assert error.original_exception is None
        assert isinstance(error, PictureError)
        assert str(error) == message

    def test_picture_upload_error_instantiation_with_original_exception(self):
        """It should test PictureUploadError with an original exception."""
        message = 'Upload failed'
        original_exception = OSError('File not found')
        error = PictureUploadError(message, original_exception)
        assert error.message == message
        assert error.original_exception == original_exception
        assert isinstance(error, PictureError)
        assert str(error) == message


class TestInvalidInputError:
    """The InvalidInputError Class Tests."""

    def test_invalid_input_error_instantiation(self):
        """It should test that InvalidInputError can be instantiated
         with a message."""
        message = 'Invalid input provided.'
        error = InvalidInputError(message)
        assert error.message == message
        assert error.original_exception is None
        assert isinstance(error, PictureError)
        assert str(error) == message

    def test_invalid_input_error_instantiation_with_original_exception(self):
        """It should test InvalidInputError with an original exception."""
        message = 'Invalid input'
        original_exception = TypeError('Incorrect type')
        error = InvalidInputError(message, original_exception)
        assert error.message == message
        assert error.original_exception == original_exception
        assert isinstance(error, PictureError)
        assert str(error) == message
