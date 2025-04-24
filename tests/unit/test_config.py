"""
Configs Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
import os

import pytest
from cba_core_lib.utils.env_utils import get_bool_from_env
from pydantic import ValidationError

from service.configs import AppConfig, MinioConfig, MongoConfig


class TestAppConfig:
    """AppConfig Class Tests."""

    @pytest.fixture
    def app_config(self):
        """Fixture to create an AppConfig instance."""
        return AppConfig()

    def test_app_config_defaults(
            self,
            app_config
    ):
        """It should verify default AppConfig attribute values."""
        assert app_config.api_version == 'v1'
        assert app_config.name == 'picture-service'
        assert app_config.description == 'REST API Service for Pictures'
        assert app_config.version == '1.0.0'
        assert app_config.log_level == 'INFO'
        assert app_config.swagger_enabled is True

        assert app_config.file_storage_provider == 'minio'

    def test_app_config_custom_values(
            self,
            monkeypatch
    ):
        """It should verify AppConfig attributes with custom environment
        variables."""
        monkeypatch.setenv('API_VERSION', 'v2')
        monkeypatch.setenv('NAME', 'image-processor')
        monkeypatch.setenv('DESCRIPTION', 'Image processing service')
        monkeypatch.setenv('VERSION', '2.5.0')
        monkeypatch.setenv('LOG_LEVEL', 'INFO')
        monkeypatch.setenv('SWAGGER_ENABLED', 'False')

        monkeypatch.setenv('FILE_STORAGE_PROVIDER', 'minio')

        app_config = AppConfig()
        # General
        assert app_config.api_version == 'v2'
        assert app_config.name == 'image-processor'
        assert app_config.description == 'Image processing service'
        assert app_config.version == '2.5.0'
        assert app_config.log_level == 'INFO'
        assert app_config.swagger_enabled is False
        # File Storage Provider
        assert app_config.file_storage_provider == 'minio'

    def test_app_config_immutability(
            self,
            app_config
    ):
        """It should ensure AppConfig instance is immutable."""
        # General
        with pytest.raises(ValidationError):
            app_config.api_version = 'v3'
        with pytest.raises(ValidationError):
            app_config.name = 'new-name'
        with pytest.raises(ValidationError):
            app_config.description = 'new description'
        with pytest.raises(ValidationError):
            app_config.version = '3.0.0'
        with pytest.raises(ValidationError):
            app_config.log_level = 'DEBUG'
        with pytest.raises(ValidationError):
            app_config.swagger_enabled = True
        # File Storage Provider
        with pytest.raises(ValidationError):
            app_config.file_storage_provider = 'aws'

    def test_app_config_post_init_sets_attributes(
            self,
            monkeypatch,
            app_config
    ):
        """It should verify attribute existence after init with custom
        env vars."""
        # General
        monkeypatch.setenv('API_VERSION', 'v2')
        monkeypatch.setenv('NAME', 'image-processor')
        monkeypatch.setenv('DESCRIPTION', 'Image processing service')
        monkeypatch.setenv('VERSION', '2.5.0')
        monkeypatch.setenv('LOG_LEVEL', 'INFO')
        monkeypatch.setenv('SWAGGER_ENABLED', 'False')

        assert hasattr(app_config, 'api_version')
        assert hasattr(app_config, 'name')
        assert hasattr(app_config, 'description')
        assert hasattr(app_config, 'version')
        assert hasattr(app_config, 'log_level')
        assert hasattr(app_config, 'swagger_enabled')

        # File Storage Provider
        monkeypatch.setenv('FILE_STORAGE_PROVIDER', 'minio')

        assert hasattr(app_config, 'file_storage_provider')

    def test_app_config_post_init_correct_values(
            self,
            app_config
    ):
        """It should verify init sets attributes to correct env var
        values."""
        # General
        assert app_config.api_version == os.getenv('API_VERSION', 'v1')
        assert app_config.name == os.getenv('NAME', 'picture-service')
        assert app_config.description == os.getenv(
            'DESCRIPTION',
            'REST API Service for Pictures'
        )
        assert app_config.version == os.getenv('VERSION', '1.0.0')
        assert app_config.log_level == os.getenv('LOG_LEVEL', 'INFO')
        assert app_config.swagger_enabled == get_bool_from_env(
            'SWAGGER_ENABLED',
            False
        )
        # File Storage Provider
        assert app_config.file_storage_provider == os.getenv(
            'FILE_STORAGE_PROVIDER',
            'minio'
        )


class TestMinioConfig:
    """The MinioConfig Class Tests."""

    @pytest.fixture
    def minio_config(self):
        """Fixture to create an MinioConfig instance."""
        return MinioConfig()

    def test_minio_config_defaults(
            self,
            minio_config
    ):
        """It should verify default MinioConfig attribute values."""
        assert str(minio_config.endpoint) == 'http://localhost:9000/'
        assert minio_config.access_key.get_secret_value() == 'admin'
        assert minio_config.secret_key.get_secret_value() == 'minio12345'
        assert minio_config.use_ssl is False

    def test_minio_config_custom_values(
            self,
            monkeypatch
    ):
        """It should verify MinioConfig attributes with custom
        environment variables."""
        monkeypatch.setenv('MINIO_ENDPOINT', 'http://localhost:9000')
        monkeypatch.setenv('MINIO_ACCESS_KEY', 'admin')
        monkeypatch.setenv('MINIO_SECRET_KEY', 'minio12345')
        monkeypatch.setenv('MINIO_USE_SSL', 'False')

        minio_config = MinioConfig()

        assert str(minio_config.endpoint) == 'http://localhost:9000/'
        assert minio_config.access_key.get_secret_value() == 'admin'
        assert minio_config.secret_key.get_secret_value() == 'minio12345'
        assert minio_config.use_ssl is False

    def test_minio_config_immutability(
            self,
            minio_config
    ):
        """It should ensure MinioConfig instance is immutable."""
        with pytest.raises(ValidationError):
            minio_config.endpoint = 'new-endpoint'
        with pytest.raises(ValidationError):
            minio_config.access_key = 'new-access-key'
        with pytest.raises(ValidationError):
            minio_config.secret_key = 'new-secret-key'
        with pytest.raises(ValidationError):
            minio_config.use_ssl = True

    def test_minio_config_init_sets_attributes(
            self,
            monkeypatch,
            minio_config
    ):
        """It should verify attribute existence after init with custom
        env vars."""
        monkeypatch.setenv('MINIO_ENDPOINT', 'http://localhost:9000')
        monkeypatch.setenv('MINIO_ACCESS_KEY', 'admin')
        monkeypatch.setenv('MINIO_SECRET_KEY', 'minio12345')
        monkeypatch.setenv('MINIO_USE_SSL', 'False')

        assert hasattr(minio_config, 'endpoint')
        assert hasattr(minio_config, 'access_key')
        assert hasattr(minio_config, 'secret_key')
        assert hasattr(minio_config, 'use_ssl')

    def test_minio_config_init_correct_values(
            self,
            minio_config
    ):
        """It should verify init sets attributes to correct env var
        values."""
        expected_endpoint_part = os.getenv(
            'MINIO_ENDPOINT',
            'http://localhost:9000'
        )
        assert expected_endpoint_part in str(minio_config.endpoint)
        assert minio_config.access_key.get_secret_value() == os.getenv(
            'MINIO_ACCESS_KEY',
            'admin'
        )
        assert minio_config.secret_key.get_secret_value() == os.getenv(
            'MINIO_SECRET_KEY',
            'minio12345'
        )
        assert minio_config.use_ssl == get_bool_from_env(
            'MINIO_USE_SSL',
            False
        )

    def test_minio_config_invalid_type_env_var(
            self,
            monkeypatch
    ):
        """It should raise ValidationError for invalid data types."""
        monkeypatch.setenv('MINIO_ENDPOINT', 'this-is-not-a-valid-url')

        with pytest.raises(ValidationError) as excinfo:
            MinioConfig()

        assert (
                'Input should be a valid URL' in str(excinfo.value) or
                'invalid URL format' in str(excinfo.value)
        )

    def test_minio_config_secure_true_variations(
            self,
            monkeypatch
    ):
        """It should set 'use_ssl' flag correctly for 'true'/'1'."""
        true_values = ['true', 'True', '1', 'TRUE']
        for true_val in true_values:
            monkeypatch.setenv('MINIO_USE_SSL', true_val)
            config = MinioConfig()
            assert config.use_ssl is True, f"Failed for MINIO_SECURE='{true_val}'"

    def test_minio_config_secure_false_variations(
            self,
            monkeypatch
    ):
        """It should set 'use_ssl' flag correctly for 'false'/'0'."""
        false_values = ['false', 'False', '0', 'FALSE']
        for false_val in false_values:
            monkeypatch.setenv('MINIO_USE_SSL', false_val)
            config = MinioConfig()
            assert config.use_ssl is False, f"Failed for MINIO_SECURE='{false_val}'"


class TestMongoConfig:
    """The MongoConfig Class Tests."""

    @pytest.fixture
    def mongo_config(self):
        """Fixture to create an MongoConfig instance."""
        return MongoConfig()

    def test_mongo_config_defaults(
            self,
            mongo_config
    ):
        """It should verify default MongoConfig attribute values."""
        assert mongo_config.uri.get_secret_value() == 'mongodb://localhost:27017'
        assert mongo_config.db_name.get_secret_value() == 'file_metadata'
        assert mongo_config.collection_name.get_secret_value() == 'uploads'

    def test_mongo_config_custom_values(
            self,
            monkeypatch
    ):
        """It should verify MongoConfig attributes with custom
        environment variables."""
        monkeypatch.setenv('MONGO_URI', 'mongodb://localhost:27017')
        monkeypatch.setenv('MONGO_DB_NAME', 'file_metadata')
        monkeypatch.setenv('MONGO_COLLECTION_NAME', 'uploads')

        mongo_config = MongoConfig()

        assert (
                mongo_config.uri.get_secret_value() ==
                'mongodb://localhost:27017'
        )
        assert mongo_config.db_name.get_secret_value() == 'file_metadata'
        assert mongo_config.collection_name.get_secret_value() == 'uploads'

    def test_mongo_config_immutability(
            self,
            mongo_config
    ):
        """It should ensure MongoConfig instance is immutable."""
        with pytest.raises(ValidationError):
            mongo_config.uri = 'new-uri'
        with pytest.raises(ValidationError):
            mongo_config.db_name = 'new-db-name'
        with pytest.raises(ValidationError):
            mongo_config.collection_name = 'new-collection-name'

    def test_mongo_config_init_sets_attributes(
            self,
            monkeypatch,
            mongo_config
    ):
        """It should verify attribute existence after init with custom
        env vars."""
        monkeypatch.setenv('MONGO_URI', 'mongodb://localhost:27017')
        monkeypatch.setenv('MONGO_DB_NAME', 'file_metadata')
        monkeypatch.setenv('MONGO_COLLECTION_NAME', 'uploads')

        assert hasattr(mongo_config, 'uri')
        assert hasattr(mongo_config, 'db_name')
        assert hasattr(mongo_config, 'collection_name')

    def test_mongo_config_init_correct_values(
            self,
            mongo_config
    ):
        """It should verify init sets attributes to correct env var
        values."""
        assert mongo_config.uri.get_secret_value() == os.getenv(
            'MONGO_URI',
            'mongodb://localhost:27017'
        )
        assert mongo_config.db_name.get_secret_value() == os.getenv(
            'MONGO_DB_NAME',
            'file_metadata'
        )
        assert mongo_config.collection_name.get_secret_value() == os.getenv(
            'MONGO_COLLECTION_NAME',
            'uploads'
        )
