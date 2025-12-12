"""
Logging configuration for PaintMatch-AI.

Provides structured, readable logging with consistent formatting
across the application. Uses Python's built-in logging module.
"""

import logging
import sys
from typing import Literal

_LOGGING_CONFIGURED = False

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO",
) -> None:
    """
    Configure structured logging for the application.

    Args:
        level: The minimum log level to capture.

    This function is idempotent - calling it multiple times
    will not add duplicate handlers.
    """
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return

    log_level = getattr(logging, level.upper(), logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Console handler with structured format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    # Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("langchain").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)

    _LOGGING_CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: The name for the logger, typically __name__ of the module.

    Returns:
        A configured Logger instance.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    # Ensure logging is configured
    if not _LOGGING_CONFIGURED:
        setup_logging()

    return logging.getLogger(name)
