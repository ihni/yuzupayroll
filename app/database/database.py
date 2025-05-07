import logging
import time
import mysql.connector

# set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# log to shell
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


class Database:
    def __init__(self, host=None, user=None, password=None, database=None, port=None, attempts=None, delay=None):
        self.config = {
            "host": host if host else "localhost",
            "user": user if user else "user",
            "password": password if password else "user",
            "database": database if database else "none",
            "port": port if port else 3306,
        }
        self.attempts = attempts if attempts else 3
        self.delay = delay if delay else 2
        self.connection = None

    def __connect(self):
        """
        private function used by self.get_connection() to set up the connector with mysql, 
        uses progressive delays to ensure the connection to the db
        """
        attempt = 1
        while attempt < self.attempts + 1:
            try:
                return mysql.connector.connect(**self.config)
            except (mysql.connector.Error, IOError) as err:
                if self.attempts == attempt:
                    logger.info("Failed to connect, exiting without a connection: %s", err)
                    return None
                logger.info(
                    "Connection failed: %s. Retrying (%d/%d)...",
                    err,
                    attempt,
                    self.attempts - 1
                )
                # exponential delay
                time.sleep(self.delay ** attempt)
                attempt += 1
        logger.error("All connection attempts failed.")
        return None

    def get_connection(self):
        """
        public function of database, returns connection if connection was
        already done else the connection will begin and the connector will
        be returned
        """
        if self.connection and self.connection.is_connected():
            return self.connection
        else:
            self.connection = self.__connect()
            if self.connection and self.connection.is_connected():
                print("Connection successful! Returning the connection...")
                return self.connection
            print("Could not connect to MySQL.")
            return None
        
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def __del__(self):
        self.close_connection()