"""
Application Global Configuration.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


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

    def __post_init__(self) -> None:
        """Post-initialization to set derived attributes and validate configuration.

        Sets the api_version, name, description and version attributes.
        """
        api_version = os.getenv('API_VERSION', 'v1')
        name = os.getenv('NAME', 'picture-service')
        description = os.getenv('DESCRIPTION', 'REST API Service for Pictures')
        version = os.getenv('VERSION', '1.0.0')
        log_level = os.getenv('LOG_LEVEL', 'INFO')

        object.__setattr__(self, 'api_version', api_version)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)
        object.__setattr__(self, 'version', version)
        object.__setattr__(self, 'log_level', log_level)
