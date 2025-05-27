import logging
from logging.handlers import RotatingFileHandler
from app.config import LoggerConfig

def get_logger(name=__name__):
    logger = logging.getLogger(name)

    # defaults to level info
    logger.setLevel(
        getattr(
            logging, 
            LoggerConfig.LOG_LEVEL.upper(), 
            logging.INFO
        )
    )

    if not logger.handlers:
        formatter = logging.Formatter(LoggerConfig.LOG_FORMATTER)

        # Log to stdout
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Log to file with rotation
        file_handler = RotatingFileHandler(
            LoggerConfig.LOG_PATH,
            **LoggerConfig.LOG_ROTATION,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
