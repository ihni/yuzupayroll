from .database import DB

class Config:
    
    # Format
    # dialect://username:password@host:port/database
    
    SQLALCHEMY_DATABASE_URI = (
        f"{DB.CONFIG['dialect']}+"
        f"{DB.CONFIG['driver']}://"
        f"{DB.CONFIG['user']}:"
        f"{DB.CONFIG['password']}@"
        f"{DB.CONFIG['host']}:"
        f"{DB.CONFIG['port']}/"
        f"{DB.CONFIG['database']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JINJA_SILENT_UNDEFINED = True # False to use StrictUndefined