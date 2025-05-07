# Logs

## Purpose
document logging configuration used in this project, such as how they are generated, where are they stored,
and how to use the logging utility

## Setup
- It is defined in app/utils/logger/logger.py and uses built-in logging module
- logs messages to both **stdout** and **log files** in (logs/app.log)
- logs are automatically cleaned up and rotated
- behaviours can be changed in `app/config/config.py`

## Use
To use the logger in any module:
```python
from app.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("This is an info message")
logger.error("This is an error")
```