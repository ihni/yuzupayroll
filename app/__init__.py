from .database import Database
from .config import (
    DATABASE_CONFIG,
    RECONNECTION_DELAY,
    CONNECTION_ATTEMPTS
)
db = Database(
    **DATABASE_CONFIG, 
    attempts=CONNECTION_ATTEMPTS, 
    delay=RECONNECTION_DELAY
)