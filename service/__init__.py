"""
Package: service.

Package for the application functionality.
"""
from __future__ import annotations

import logging

from cba_core_lib.logging import init_logging
from service.configs import AppConfig

# Application configuration
app_config = AppConfig()

# Get the root logger
logger = logging.getLogger()

# Initialize logging with the root logger.
# The logging configuration sets the application's logger to DEBUG level.
# This will affect all loggers in the application.
init_logging(logger, log_level=app_config.log_level)
