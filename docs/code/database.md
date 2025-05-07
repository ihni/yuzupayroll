# Database File

## Structure
- Contains a class used to initialize and return the connection to the MySQL. 
- The initialization of a database only happens once in the init file where the configuration is passed from the config file

## Use
- The only exposed functions are **get_connection()** and **close_connection()**
- The former will connect if no connections were made(or reconnect if it had previously failed) and return the connector, else,
  previous connection still existed, that would then be returned
- **close_connection()** automatically cleans up the connection and closes it
- import the db package and get the connection like such:
```python
from database import db
cnx = db.get_connection()
```