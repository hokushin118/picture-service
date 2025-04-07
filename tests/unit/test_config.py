"""
Configs Unit Test Suite.

Test cases can be run with the following:
  pytest -v --cov=service --cov-report=term-missing --cov-branch
"""
import os

import pytest

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

    def test_app_config_custom_values(self, monkeypatch):
        """It should verify AppConfig attributes with custom environment
        variables."""
        monkeypatch.setenv('API_VERSION', 'v2')
        monkeypatch.setenv('NAME', 'image-processor')
        monkeypatch.setenv('DESCRIPTION', 'Image processing service')
        monkeypatch.setenv('VERSION', '2.5.0')

        app_config = AppConfig()
        assert app_config.api_version == 'v2'
        assert app_config.name == 'image-processor'
        assert app_config.description == 'Image processing service'
        assert app_config.version == '2.5.0'

    def test_app_config_immutability(self, app_config):
        """It should ensure AppConfig instance is immutable."""
        with pytest.raises(AttributeError):
            app_config.api_version = 'v3'

    def test_app_config_post_init_sets_attributes(
            self,
            monkeypatch,
            app_config
    ):
        """It should verify attribute existence after post_init with custom
        env vars."""
        monkeypatch.setenv('API_VERSION', 'v2')
        monkeypatch.setenv('NAME', 'image-processor')
        monkeypatch.setenv('DESCRIPTION', 'Image processing service')
        monkeypatch.setenv('VERSION', '2.5.0')

        assert hasattr(app_config, 'api_version')
        assert hasattr(app_config, 'name')
        assert hasattr(app_config, 'description')
        assert hasattr(app_config, 'version')

    def test_app_config_post_init_correct_values(self, app_config):
        """It should verify post_init sets attributes to correct env var
        values."""
        assert app_config.api_version == os.getenv('API_VERSION', 'v1')
        assert app_config.name == os.getenv('NAME', 'picture-service')
        assert app_config.description == os.getenv(
            'DESCRIPTION',
            'REST API Service for Pictures'
        )
        assert app_config.version == os.getenv('VERSION', '1.0.0')
