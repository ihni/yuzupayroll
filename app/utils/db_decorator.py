from mysql.connector import Error as MySQLError
from .. import db
from . import get_logger, ErrorCodes
from functools import wraps

logger = get_logger(__name__)

class DBError(Exception):
    """Custom exception for database errors."""
    pass

def db_operation(commit=False, fetch=False, fetch_many=False):
    """Decorator to manage DB connections, transactions, and cursor handling.

    Args:
        commit (bool): If True, commits changes after successful execution.
        fetch (bool): If True, fetches results (use with SELECT queries).
        fetch_many (bool): If True, fetches all rows; else fetches one.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cnx = None
            cursor = None
            try:
                cnx = db.get_connection()
                if not cnx:
                    error_code = ErrorCodes.DB_CONNECTION_FAILED
                    logger.error(f"{error_code}: No database connection available.")
                    raise DBError(
                        ErrorCodes.DB_CONNECTION_FAILED, 
                        "Database connection failed"
                    )
            
                cursor = cnx.cursor(dictionary=kwargs.pop("dict_cursor", True))
                result = func(cursor, *args, **kwargs)

                if commit:
                    cnx.commit()

                if fetch:
                    return cursor.fetchone() if not fetch_many else cursor.fetchall()
                
                return result
            
            except MySQLError as err:
                if cnx and commit:
                    cnx.rollback()
                error_code = ErrorCodes.DB_QUERY_FAILED
                logger.error(f"{error_code}: DB operation failed in {func.__name__}: {err}")
                raise DBError(ErrorCodes.DB_QUERY_FAILED, str(err))
            finally:
                if cursor:
                    cursor.close()
                if cnx:
                    cnx.close_connection()    
        return wrapper
    return decorator