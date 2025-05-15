import os

MEGABYTES = 5 # for max file space

class LoggerConfig:
    LOG_LEVEL = "INFO"          # INFO, DEBUG, WARNING, ERROR, CRITICAL
    LOG_DIR = '/storage/logs'   # Container path (mounted from ./storage/logs)
    LOG_FILE = 'app.log'
    LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)
    LOG_ENCODING = 'utf-8'
    os.makedirs(LOG_DIR, exist_ok=True)

    LOG_ROTATION = {
        "maxBytes": MEGABYTES * (1024 * 1024),
        "backupCount": 3
    } 

    LOG_FORMATTER = (
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )