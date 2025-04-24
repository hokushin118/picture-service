"""
Package: service.

Package for the application functionality.
"""
from __future__ import annotations

import logging
import os
import pathlib

from cba_core_lib.logging import init_logging
from dotenv import load_dotenv

from service.configs import AppConfig

# Get the root logger
logger = logging.getLogger()

BASE_DIR = pathlib.Path(__file__).resolve().parent
"""Path to the base directory of the microservice."""


# --- Configuration and Environment Setup ---

def load_environment_variables() -> None:
    """Loads environment variables from a .env file into the operating system's
    environment.

    This function uses the `dotenv` library to load key-value pairs from a
    .env file located in the current working directory and sets them as
    environment variables. This allows the application to access configuration
    settings without hardcoding them in the source code.

    Returns:
        None: This function modifies the operating system's environment and
        does not return a value.
    """
    # Load the correct .env file based on APP_SETTINGS
    # export APP_SETTINGS=docker  # Or production, etc.
    env = os.environ.get('APP_SETTINGS')
    logging.warning("Environment variables: %s", env)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dotenv_filename = '.env' if not env else f'.env.{env}'
    dotenv_path = os.path.join(base_dir, dotenv_filename)
    logger.debug("Loading environment variables from: %s", dotenv_path)
    try:
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            logger.info("Environment variables loaded from %s", dotenv_path)
        else:
            logger.warning("Dotenv file not found at %s", dotenv_path)
    except FileNotFoundError as err:
        logging.error(
            "Dotenv file not found: %s: %s",
            dotenv_path,
            err
        )
    except UnicodeDecodeError as err:
        logging.error(
            "Encoding error in dotenv file: %s: %s",
            dotenv_path,
            err
        )
    except OSError as err:
        logging.error(
            "OS error reading dotenv file: %s: %s",
            dotenv_path,
            err
        )
    except SyntaxError as err:
        logging.error(
            "Syntax error in dotenv file: %s: %s",
            dotenv_path,
            err
        )
    except TypeError as err:
        logging.error(
            "Type error while loading dotenv file: %s: %s",
            dotenv_path,
            err
        )


# Load environment at startup
load_environment_variables()

# Application configuration
app_config = AppConfig()

# Initialize logging with the root logger.
# The logging configuration sets the application's logger to DEBUG level.
# This will affect all loggers in the application.
init_logging(logger, log_level=app_config.log_level)
