# Database File

## Structure
- Contains a class used to initialize and return the connection to the MySQL. 
- The initialization of a database only happens once in the init file where the configuration is passed from the config file

## Use
- The only exposed functions are **get_connection()** and **close_connection()**
- The former will connect if no connections were made(or reconnect if it had previously failed) and return the connector, else,
  the previous connection still that existed would then be returned
- **close_connection()** automatically cleans up the connection and closes it
- import the db package and get the connection like such:
```python
from database import db
cnx = db.get_connection()
```

## Other functions

### `db_operation` decorator
**File**: `app/utils/db_decorator.py`
**Purpose**: abstract and standardize database connection handling, error management, and cursor operations(used principally in the service layer)

#### Usage
Basic usage patterns:
- Query operations: Enable `fetch` with optional `fetch_many`  
- Write operations: Enable `commit` for auto-commit  

```python
# For queries (auto-fetch single row)
@db_operation(fetch=True)
def get_user(cursor, user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# For updates (auto-commit)
@db_operation(commit=True)
def update_user(cursor, user_id, name):
    cursor.execute("UPDATE users SET name=%s WHERE id=%s", (name, user_id))

# For batch fetching
@db_operation(fetch=True, fetch_many=True) 
def get_all_active_users(cursor):
    cursor.execute("SELECT * FROM users WHERE is_active=1")
```

#### Parameters

| Parameter  | Type    | Default | Description |
|------------|---------|---------|-------------|
| `commit`   | `bool`  | `False` | Enables transaction commit |
| `fetch`    | `bool`  | `False` | Enables result fetching |
| `fetch_many` | `bool` | `False` | Fetches multiple rows |

#### Error Codes

| Code                   | Description                     |
|------------------------|---------------------------------|
| `DB_CONNECTION_FAILED` | Connection establishment failed |
| `DB_QUERY_FAILED`      | SQL query execution failed      |
