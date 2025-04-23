"""
Configs Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
import os

import pytest
from cba_core_lib.utils.env_utils import get_bool_from_env

from service.configs import AppConfig


class TestAppConfig:
    """AppConfig Class Tests."""

    @pytest.fixture
    def app_config(self):
        """Fixture to create an AppConfig instance."""
        return AppConfig()

    def test_app_config_defaults(self, app_config):
        """It should verify default AppConfig attribute values."""
        assert app_config.api_version == 'v1'
        assert app_config.name == 'picture-service'
        assert app_config.description == 'REST API Service for Pictures'
        assert app_config.version == '1.0.0'
        assert app_config.log_level == 'INFO'

        assert app_config.minio_endpoint == 'localhost:9000'
        assert app_config.minio_access_key == 'admin'
        assert app_config.minio_secret_key == 'minio12345'
        assert app_config.minio_bucket == 'picture-service-data'
        assert app_config.minio_use_ssl is False

    def test_app_config_custom_values(self, monkeypatch):
        """It should verify AppConfig attributes with custom environment
        variables."""
        monkeypatch.setenv('API_VERSION', 'v2')
        monkeypatch.setenv('NAME', 'image-processor')
        monkeypatch.setenv('DESCRIPTION', 'Image processing service')
        monkeypatch.setenv('VERSION', '2.5.0')
        monkeypatch.setenv('LOG_LEVEL', 'INFO')

        monkeypatch.setenv('MINIO_ENDPOINT', 'localhost:9000')
        monkeypatch.setenv('MINIO_ACCESS_KEY', 'admin')
        monkeypatch.setenv('MINIO_SECRET_KEY', 'minio12345')
        monkeypatch.setenv('MINIO_BUCKET', 'picture-service-data')
        monkeypatch.setenv('MINIO_USE_SSL', 'False')

        app_config = AppConfig()
        # General
        assert app_config.api_version == 'v2'
        assert app_config.name == 'image-processor'
        assert app_config.description == 'Image processing service'
        assert app_config.version == '2.5.0'
        assert app_config.log_level == 'INFO'
        # MinIO
        assert app_config.minio_endpoint == 'localhost:9000'
        assert app_config.minio_access_key == 'admin'
        assert app_config.minio_secret_key == 'minio12345'
        assert app_config.minio_bucket == 'picture-service-data'
        assert app_config.minio_use_ssl is False

    def test_app_config_immutability(self, app_config):
        """It should ensure AppConfig instance is immutable."""
        # General
        with pytest.raises(AttributeError):
            app_config.api_version = 'v3'
        with pytest.raises(AttributeError):
            app_config.name = 'new-name'
        with pytest.raises(AttributeError):
            app_config.description = 'new description'
        with pytest.raises(AttributeError):
            app_config.version = '3.0.0'
        with pytest.raises(AttributeError):
            app_config.log_level = 'DEBUG'
        # MinIO
        with pytest.raises(AttributeError):
            app_config.minio_endpoint = 'minio:9000'
        with pytest.raises(AttributeError):
            app_config.minio_access_key = 'new-key'
        with pytest.raises(AttributeError):
            app_config.minio_secret_key = 'new-secret-key'
        with pytest.raises(AttributeError):
            app_config.minio_bucket = 'new-bucket'
        with pytest.raises(AttributeError):
            app_config.minio_use_ssl = True

    def test_app_config_post_init_sets_attributes(
            self,
            monkeypatch,
            app_config
    ):
        """It should verify attribute existence after post_init with custom
        env vars."""
        # General
        monkeypatch.setenv('API_VERSION', 'v2')
        monkeypatch.setenv('NAME', 'image-processor')
        monkeypatch.setenv('DESCRIPTION', 'Image processing service')
        monkeypatch.setenv('VERSION', '2.5.0')
        monkeypatch.setenv('LOG_LEVEL', 'INFO')

        assert hasattr(app_config, 'api_version')
        assert hasattr(app_config, 'name')
        assert hasattr(app_config, 'description')
        assert hasattr(app_config, 'version')
        assert hasattr(app_config, 'log_level')

        # MinIO
        monkeypatch.setenv('MINIO_ENDPOINT', 'localhost:9000')
        monkeypatch.setenv('MINIO_ACCESS_KEY', 'admin')
        monkeypatch.setenv('MINIO_SECRET_KEY', 'minio12345')
        monkeypatch.setenv('MINIO_BUCKET', 'picture-service-data')
        monkeypatch.setenv('MINIO_USE_SSL', 'False')

        assert hasattr(app_config, 'minio_endpoint')
        assert hasattr(app_config, 'minio_access_key')
        assert hasattr(app_config, 'minio_secret_key')
        assert hasattr(app_config, 'minio_bucket')
        assert hasattr(app_config, 'minio_use_ssl')

    def test_app_config_post_init_correct_values(self, app_config):
        """It should verify post_init sets attributes to correct env var
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
        # MinIO
        assert app_config.minio_endpoint == os.getenv(
            'MINIO_ENDPOINT',
            'localhost:9000'
        )
        assert app_config.minio_access_key == os.getenv(
            'MINIO_ACCESS_KEY',
            'admin'
        )
        assert app_config.minio_secret_key == os.getenv(
            'MINIO_SECRET_KEY',
            'minio12345'
        )
        assert app_config.minio_bucket == os.getenv(
            'MINIO_BUCKET',
            'picture-service-data'
        )
        assert app_config.minio_use_ssl == get_bool_from_env(
            'MINIO_USE_SSL',
            False
        )
