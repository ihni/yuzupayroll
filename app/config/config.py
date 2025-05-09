"""
THE SETTINGS ARE OPEN FOR ACADEMIC 
REASONS, NO NEED FOR A SEPERATE .env
"""

import os

"""
FOR DATABASE CONFIGURATION
"""

DATABASE_CONFIG = {
    "host" : "db",
    "user" : "user",
    "password" : "pass",
    "database" : "payroll_db",
    "port" : 3306
}

# number of times to connect and delay in seconds
CONNECTION_ATTEMPTS = 6
RECONNECTION_DELAY = 2


"""
FOR SQLALCHEMY CONFIGURATION
"""

class Config:
    #SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_CONFIG["user"]}:{DATABASE_CONFIG["password"]}@{DATABASE_CONFIG["host"]}/{DATABASE_CONFIG["database"]}"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://user:password@db/payroll_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


"""
FOR LOGGER CONFIGURATION
"""

class LoggerConfig:
    LOG_LEVEL = "INFO" # INFO, DEBUG, WARNING, ERROR, CRITICAL
    LOG_DIR = '/storage/logs'  # Container path (mounted from ./storage/logs)
    LOG_FILE = 'app.log'
    LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)
    LOG_ENCODING = 'utf-8'
    os.makedirs(LOG_DIR, exist_ok=True)

    LOG_ROTATION = {
        "maxBytes": 5 * (1024 * 1024), # in megabytes
        "backupCount": 3
    } 

    LOG_FORMATTER = (
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )