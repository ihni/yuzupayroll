from .database import Database
from ..config import DATABASE_CONFIG

db = Database(**DATABASE_CONFIG)