"""
Lightweight logging helper.

Wraps the stdlib logging module with a sensible default format and exposes a
single `get_logger` function so every module in this project uses the same
configuration.
"""

import logging
import sys


def get_logger(name: str = "file_organizer", verbose: bool = False) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: Logger name, typically the module name.
        verbose: When True, emit DEBUG-level messages too.
    """
    logger = logging.getLogger(name)

    # Avoid attaching duplicate handlers if get_logger is called more than once.
    if logger.handlers:
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)-7s %(message)s", "%H:%M:%S")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger
