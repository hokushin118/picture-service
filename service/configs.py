"""
Application Global Configuration.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from pydantic import AnyHttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


######################################################################
# APPLICATION CONFIGURATION
######################################################################
@dataclass(frozen=True)
class AppConfig:
    """Encapsulates application configuration settings, including database
    and runtime parameters.

    Retrieves settings from environment variables with sensible defaults.

    This class is immutable.
    """
    # General Settings
    api_version: str = field(init=False)
    """The version of the API, retrieved from the API_VERSION environment variable."""

    name: str = field(init=False)
    """The name of the application, retrieved from the NAME
    environment variable."""

    description: str = field(init=False)
    """The description of the application, retrieved from the NAME
    environment variable."""

    version: str = field(init=False)
    """The version of the application, retrieved from the VERSION
    environment variable."""

    log_level: str = field(init=False)
    """Log level of the application, retrieved from the LOG_LEVEL
    environment variable."""

    file_storage_provider: str = field(init=False)
    """File storage provider."""

    def __post_init__(self) -> None:
        """Post-initialization to set derived attributes and validate configuration.

        Sets the api_version, name, description and version attributes.
        """
        api_version: str = os.getenv('API_VERSION', 'v1')
        name: str = os.getenv('NAME', 'picture-service')
        description: str = os.getenv(
            'DESCRIPTION',
            'REST API Service for Pictures'
        )
        version: str = os.getenv('VERSION', '1.0.0')
        log_level: str = os.getenv('LOG_LEVEL', 'INFO')

        # File Storage Provider Choice
        file_storage_provider: str = os.getenv(
            'FILE_STORAGE_PROVIDER',
            'minio'
        )

        object.__setattr__(self, 'api_version', api_version)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)
        object.__setattr__(self, 'version', version)
        object.__setattr__(self, 'log_level', log_level)

        object.__setattr__(
            self,
            'file_storage_provider',
            file_storage_provider
        )


class MinioConfig(BaseSettings):
    """Encapsulates MinIO file storage configuration settings (Pydantic V2).

    Retrieves settings from environment variables with sensible defaults.
    Secrets are handled using Pydantic's SecretStr type.

    This class is immutable.
    """

    endpoint: AnyHttpUrl
    access_key: SecretStr
    secret_key: SecretStr
    use_ssl: bool = False

    model_config = SettingsConfigDict(
        env_prefix='minio_',
        case_sensitive=False,
        extra='ignore',
        frozen=True,
    )


class MongoConfig(BaseSettings):
    """Encapsulates MongoDB configuration settings (Pydantic V2).

    Retrieves settings from environment variables with sensible defaults.
    Secrets are handled using Pydantic's SecretStr type.

    This class is immutable.
    """

    uri: SecretStr
    db_name: SecretStr
    collection_name: SecretStr

    model_config = SettingsConfigDict(
        env_prefix='mongo_',
        case_sensitive=False,
        extra='ignore',
        frozen=True,
    )
