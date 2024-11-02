import logging
import os
from typing import Optional

# Import the logging configuration from the .env file
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = os.getenv("LOG_FILE", "app.log")

# Configure the logging system
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    filename=LOG_FILE,
)

# Define the global logger
logger = logging.getLogger(__name__)

def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a logger for the given name.

    Args:
        name: The name of the logger.

    Returns:
        A logger for the specified name.
    """
    return logging.getLogger(name)