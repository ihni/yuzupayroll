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
    "password" : "user",
    "database" : "payroll_db",
    "port" : 3306
}

"""
FOR LOGGER CONFIGURATION
"""

LOG_LEVEL = "INFO" # INFO, DEBUG, WARNING, ERROR, CRITICAL
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, 'app.log')

LOG_ROTATION = {
    "maxBytes": 5 * (1024 * 1024), # in megabytes
    "backupCount": 3
} 

LOG_FORMATTER = (
    "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
)
