"""
Application Global Configuration.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from cba_core_lib.utils.env_utils import get_bool_from_env


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

    # MinIO
    minio_endpoint: str = field(init=False)
    """MinIO server endpoint (e.g., localhost:9000)."""

    minio_access_key: str = field(init=False)
    """MinIO access key."""

    minio_secret_key: str = field(init=False)
    """MinIO secret key."""

    minio_bucket: str = field(init=False)
    """MinIO bucket name for microservice data."""

    minio_use_ssl: bool = field(init=False)
    """Use SSL/TLS for MinIO connection."""

    # MongoDB
    mongo_uri: str = field(init=False)
    """MongoDB connection URI."""

    mongo_db_name: str = field(init=False)
    """MongoDB database name."""

    mongo_collection_name: str = field(init=False)
    """MongoDB database collection name."""

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

        minio_endpoint: str = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
        minio_access_key: str = os.getenv('MINIO_ACCESS_KEY', 'admin')
        minio_secret_key: str = os.getenv('MINIO_SECRET_KEY', 'minio12345')
        minio_bucket: str = os.getenv('MINIO_BUCKET', 'picture-service-data')
        minio_use_ssl: bool = get_bool_from_env(
            'MINIO_USE_SSL',
            False
        )

        mongo_uri: str = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
        mongo_db_name: str = os.getenv('MONGO_DB_NAME', 'file_metadata')
        mongo_collection_name: str = os.getenv(
            'MONGO_COLLECTION_NAME',
            'uploads'
        )

        object.__setattr__(self, 'api_version', api_version)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)
        object.__setattr__(self, 'version', version)
        object.__setattr__(self, 'log_level', log_level)

        object.__setattr__(self, 'minio_endpoint', minio_endpoint)
        object.__setattr__(self, 'minio_access_key', minio_access_key)
        object.__setattr__(self, 'minio_secret_key', minio_secret_key)
        object.__setattr__(self, 'minio_bucket', minio_bucket)
        object.__setattr__(self, 'minio_use_ssl', minio_use_ssl)

        object.__setattr__(self, 'mongo_uri', mongo_uri)
        object.__setattr__(self, 'mongo_db_name', mongo_db_name)
        object.__setattr__(self, 'mongo_collection_name', mongo_collection_name)
