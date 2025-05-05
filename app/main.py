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

def connect_to_mysql(config, attempts=3,delay=2):
    attempt = 1
    while attempt < attempts + 1:
        try:
            return mysql.connector.connect(**config)
        except (mysql.connector.Error, IOError) as err:
            if (attempts is attempt):
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts-1,
            )

            time.sleep(delay ** attempt)
            attempt += 1
    return None

config = {
    "host" : "db",
    "user" : "user",
    "password" : "user",
    "database" : "payroll_db",
    "port" : 3306,
}

cnx = connect_to_mysql(config, attempts=5, delay=3)

if cnx and cnx.is_connected():
    print("Connection successful!...")
    print(cnx)
    cnx.close()
else:
    print("Could not connect to MySQL")
