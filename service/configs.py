"""
Application Global Configuration.
"""
from __future__ import annotations

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


######################################################################
# APPLICATION CONFIGURATION
######################################################################
class AppConfig(BaseSettings):
    """Encapsulates application configuration settings, including database
    and runtime parameters.

    Retrieves settings from environment variables with sensible defaults.

    This class is immutable.
    """
    api_version: str
    """The version of the API, retrieved from the API_VERSION environment variable."""

    name: str
    """The name of the application, retrieved from the NAME
    environment variable."""

    description: str
    """The description of the application, retrieved from the NAME
    environment variable."""

    version: str
    """The version of the application, retrieved from the VERSION
    environment variable."""

    log_level: str
    """Log level of the application, retrieved from the LOG_LEVEL
    environment variable."""

    file_storage_provider: str
    """File storage provider."""

    swagger_enabled: bool
    """Whether to enable Swagger for the microservice."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra='ignore',
        frozen=True,
    )


######################################################################
# MONGODB CONFIGURATION
######################################################################
class MongoConfig(BaseSettings):
    """Encapsulates MongoDB configuration settings (Pydantic V2).

    Retrieves settings from environment variables with sensible defaults.
    Secrets are handled using Pydantic's SecretStr type.

    This class is immutable.
    """

    uri: SecretStr
    """The MongoDB connection URI."""

    db_name: SecretStr
    """The name of the MongoDB database."""

    collection_name: SecretStr
    """The name of the MongoDB collection."""

    model_config = SettingsConfigDict(
        env_prefix='mongo_',
        case_sensitive=False,
        extra='ignore',
        frozen=True,
    )
