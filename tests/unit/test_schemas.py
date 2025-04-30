"""
Schemas Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
import pytest
from pydantic import ValidationError

from service.schemas import (
    InfoDTO,
    HealthCheckDTO,
    check_not_whitespace_only,
    IndexDTO,
    UploadResponseDTO
)
from tests import (
    TEST_FILE_NAME,
    TEST_OBJECT_NAME,
    TEST_URL,
    TEST_FILE_SIZE,
    TEST_ETAG, create_upload_response_dto
)


class TestCheckNotWhitespaceOnly:
    """The check_not_whitespace_only Function Tests."""

    def test_check_not_whitespace_only_valid_string(self):
        """It should return the original string when given a valid string
        that contains non-whitespace characters."""
        test_string = 'Hello, World!'
        result = check_not_whitespace_only(test_string)
        assert result == test_string, 'Should return the original string'

    def test_check_not_whitespace_only_string_with_leading_and_trailing_spaces(
            self
    ):
        """It should return the original string when given a string that has
        leading and trailing spaces."""
        test_string = '   Trimmed String   '
        result = check_not_whitespace_only(test_string)
        assert result == test_string, \
            'Should return the original string with spaces'

    def test_check_not_whitespace_only_string_with_internal_spaces(self):
        """It should return the original string when given a string that has
        spaces within the string."""
        test_string = 'Internal Spaces String'
        result = check_not_whitespace_only(test_string)
        assert result == test_string, \
            'Should return the original string with spaces'

    def test_check_not_whitespace_only_string_with_only_spaces(self):
        """It should raise a ValueError when the string contains
        only spaces."""
        test_string = "   "
        with pytest.raises(ValueError) as excinfo:
            check_not_whitespace_only(test_string)
        assert 'Field cannot consist only of whitespace.' in str(
            excinfo.value
        ), 'Should raise ValueError with correct message'

    def test_check_not_whitespace_only_string_with_tabs(self):
        """It should raise a ValueError when the string contains only tabs."""
        test_string = "\t\t\t"
        with pytest.raises(ValueError) as excinfo:
            check_not_whitespace_only(test_string)
        assert 'Field cannot consist only of whitespace.' in str(
            excinfo.value
        ), 'Should raise ValueError with correct message'

    def test_check_not_whitespace_only_string_with_newlines(self):
        """It should raise a ValueError when the string contains only
        newlines."""
        test_string = '\n\n\n'
        with pytest.raises(ValueError) as excinfo:
            check_not_whitespace_only(test_string)
        assert 'Field cannot consist only of whitespace.' in str(
            excinfo.value
        ), 'Should raise ValueError with correct message'

    def test_check_not_whitespace_only_string_with_mixed_whitespace(self):
        """It should raise a ValueError when the string contains mixed
        whitespace characters."""
        test_string = '  \t\n  '
        with pytest.raises(ValueError) as excinfo:
            check_not_whitespace_only(test_string)
        assert 'Field cannot consist only of whitespace.' in str(
            excinfo.value
        ), 'Should raise ValueError with correct message'


class TestIndexDTO:
    """IndexDTO Schema Tests."""

    def test_indexdto_valid_message(self):
        """It should return the original values when given valid values."""
        index_dto = IndexDTO(message='Welcome to the Picture API!')
        assert index_dto.message == 'Welcome to the Picture API!'

    def test_indexdto_invalid_message(self):
        """It should ensure that providing an invalid message (e.g., a number)
        raises a ValidationError."""
        with pytest.raises(ValidationError):
            IndexDTO(message=123)

        # Test empty string - should fail due to min_length=1
        with pytest.raises(ValidationError):
            IndexDTO(message='')

        # Test None - should fail as the field is required (...)
        with pytest.raises(ValidationError):
            IndexDTO(message=None)

    def test_indexdto_missing_message(self):
        """It should confirm that omitting the 'message' field during
        initialization raises a ValidationError."""
        with pytest.raises(ValidationError):
            IndexDTO()


class TestHealthCheckDTO:
    """HealthCheckDTO Schema Tests."""

    def test_healthcheckdto_valid_status(self):
        """It should return the original values when given valid values."""
        health_check_dto = HealthCheckDTO(status='UP')
        assert health_check_dto.status == 'UP'

    def test_healthcheckdto_invalid_status(self):
        """It should ensure that providing an invalid status (e.g., a number)
        raises a ValidationError."""
        with pytest.raises(ValidationError):
            HealthCheckDTO(status=123)

        # Test empty string - should fail due to min_length=1
        with pytest.raises(ValidationError):
            HealthCheckDTO(status='')

        # Test None - should fail as the field is required (...)
        with pytest.raises(ValidationError):
            HealthCheckDTO(status=None)

    def test_healthcheckdto_missing_status(self):
        """It should confirm that omitting the 'status' field during
        initialization raises a ValidationError."""
        with pytest.raises(ValidationError):
            HealthCheckDTO()


class TestInfoDTO:
    """InfoDTO Schema Tests."""

    def test_infodto_valid_data(self):
        """It should return the original values when given valid values."""
        info_dto = InfoDTO(
            name='test_service',
            version='1.2.3',
            uptime='1 day, 0:00:00'
        )
        assert info_dto.name == 'test_service'
        assert info_dto.version == '1.2.3'
        assert info_dto.uptime == '1 day, 0:00:00'

    def test_infodto_invalid_name(self):
        """It should verify that providing an invalid data type for
        'name' (e.g., a number) raises an error."""
        with pytest.raises(ValidationError):
            InfoDTO(name=123, version='1.2.3', uptime='0:00:00')

    def test_infodto_invalid_version(self):
        """It should check that providing an invalid data type for 'version'
        (e.g., None) raises an error."""
        with pytest.raises(ValidationError):
            InfoDTO(name='test_service', version=None, uptime='0:00:00')

    def test_infodto_invalid_uptime(self):
        """It should confirm that providing an invalid data type for 'uptime'
        (e.g., a number) raises an error."""
        with pytest.raises(ValidationError):
            InfoDTO(name='test_service', version='1.2.3', uptime=123)

    def test_infodto_missing_name(self):
        """It should verify that omitting the 'name' field raises a
        ValidationError."""
        with pytest.raises(ValidationError):
            InfoDTO(version='1.2.3', uptime='0:00:00')

    def test_infodto_missing_version(self):
        """It should confirm that omitting the 'version' field raises
        a ValidationError."""
        with pytest.raises(ValidationError):
            InfoDTO(name='test_service', uptime='0:00:00')

    def test_infodto_missing_uptime(self):
        """It should check that omitting the 'uptime' field raises
        a ValidationError."""
        with pytest.raises(ValidationError):
            InfoDTO(name='test_service', version='1.2.3')


class TestUploadResponseDTO:
    """UploadResponseDTO Schema Tests."""

    def test_uploadresponsedto_valid_data(self):
        """It should return the original values when given valid values."""
        upload_response_dto = create_upload_response_dto()

        assert upload_response_dto.original_filename == TEST_FILE_NAME
        assert upload_response_dto.object_name == TEST_OBJECT_NAME
        assert str(upload_response_dto.file_url) == TEST_URL
        assert upload_response_dto.size == TEST_FILE_SIZE
        assert upload_response_dto.etag == TEST_ETAG

    def test_uploadresponsedto_invalid_original_filename(self):
        """It should verify that providing an invalid data type for
        'original_filename' (e.g., a number) raises an error."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=123,
                object_name=TEST_OBJECT_NAME,
                file_url=TEST_URL,
                size=TEST_FILE_SIZE,
                etag=TEST_ETAG
            )

    def test_infodto_invalid_object_name(self):
        """It should check that providing an invalid data type for 'object_name'
        (e.g., None) raises an error."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=TEST_FILE_NAME,
                object_name=123,
                file_url=TEST_URL,
                size=TEST_FILE_SIZE,
                etag=TEST_ETAG
            )

    def test_uploadresponsedto_invalid_file_url(self):
        """It should confirm that providing an invalid data type for 'file_url'
        (e.g., a number) raises an error."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=TEST_FILE_NAME,
                object_name=TEST_OBJECT_NAME,
                file_url=123,
                size=TEST_FILE_SIZE,
                etag=TEST_ETAG
            )

    def test_uploadresponsedto_invalid_size(self):
        """It should confirm that providing an invalid data type for 'size'
        (e.g., a number) raises an error."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=TEST_FILE_NAME,
                object_name=TEST_OBJECT_NAME,
                file_url=TEST_URL,
                size='23M',
                etag=TEST_ETAG
            )

    def test_uploadresponsedto_invalid_etag(self):
        """It should confirm that providing an invalid data type for 'etag'
        (e.g., a number) raises an error."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=TEST_FILE_NAME,
                object_name=TEST_OBJECT_NAME,
                file_url=TEST_URL,
                size=TEST_FILE_SIZE,
                etag=123
            )

    def test_uploadresponsedto_missing_original_filename(self):
        """It should verify that omitting the 'original_filename' field raises a
        ValidationError."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                object_name=TEST_OBJECT_NAME,
                file_url=TEST_URL,
                size=TEST_FILE_SIZE,
                etag=TEST_ETAG
            )

    def test_uploadresponsedto_missing_object_name(self):
        """It should confirm that omitting the 'object_name' field raises
        a ValidationError."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=TEST_FILE_NAME,
                file_url=TEST_URL,
                size=TEST_FILE_SIZE,
                etag=TEST_ETAG
            )

    def test_uploadresponsedto_missing_file_url(self):
        """It should check that omitting the 'file_url' field raises
        a ValidationError."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=TEST_FILE_NAME,
                object_name=TEST_OBJECT_NAME,
                size=TEST_FILE_SIZE,
                etag=TEST_ETAG
            )

    def test_uploadresponsedto_missing_size(self):
        """It should check that omitting the 'size' field raises
        a ValidationError."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=TEST_FILE_NAME,
                object_name=TEST_OBJECT_NAME,
                file_url=TEST_URL,
                etag=TEST_ETAG
            )

    def test_uploadresponsedto_missing_etag(self):
        """It should check that omitting the 'etag' field raises
        a ValidationError."""
        with pytest.raises(ValidationError):
            UploadResponseDTO(
                original_filename=TEST_FILE_NAME,
                object_name=TEST_OBJECT_NAME,
                file_url=TEST_URL,
                size=TEST_FILE_SIZE
            )
