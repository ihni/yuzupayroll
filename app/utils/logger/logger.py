import logging
from logging.handlers import RotatingFileHandler
from ...config import (
    LOG_LEVEL, 
    LOG_FORMATTER, 
    LOG_PATH,
    LOG_ROTATION,
)

def get_logger(name=__name__):
    # Set up logger
    logger = logging.getLogger(name)
    # defaults to level info
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    if not logger.handlers:
        formatter = logging.Formatter(LOG_FORMATTER)

        # Log to stdout
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Log to file with rotation
        file_handler = RotatingFileHandler(
            LOG_PATH,
            **LOG_ROTATION,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
