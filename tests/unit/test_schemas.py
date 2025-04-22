"""
Schemas Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
import pytest
from pydantic import ValidationError

from service.schemas import InfoDTO, HealthCheckDTO, check_not_whitespace_only, \
    IndexDTO


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
        """It should verify that a valid message string is accepted
        without errors."""
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
        """It should verify that a valid status string is accepted
        without errors."""
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
        """It should verify that providing an invalid data type for
        'name' (e.g., a number) raises an error."""
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
