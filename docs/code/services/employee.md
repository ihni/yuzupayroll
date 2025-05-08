# Employee Service

## Overview
Provides database operations for the `employees` table using the `db_operation` decorator pattern. All methods are static and thread-safe.

## Interface

### `create(cursor, employee: Employee) -> dict`
Creates a new employee record.
- **Parameters**:
  - `employee`: Validated Employee model instance
- **Returns**:
  - Dictionary with created employee ID: `{"id": int}`

### `get_by_id(cursor, emp_id: int) -> tuple`
Retrieves an employee by ID.
- **Parameters**:
  - `emp_id`: Employee ID to query
- **Returns**:
  - Tuple of `(query, params)` for decorator processing

### `get_by_email(cursor, emp_email: str) -> tuple`
Finds an employee by email address.
- **Parameters**:
  - `emp_email`: Exact email to match
- **Returns**:  
  - Tuple of `(query, params)`

### `get_by_role_id(cursor, role_id: int) -> tuple`
Lists employees with specific role ID.
- **Parameters**:
  - `role_id`: Role identifier
- **Returns**:
  - Tuple for multi-row query

### `get_by_role_name(cursor, role_name: str) -> tuple`
Searches employees by role name pattern.
- **Parameters**:
  - `role_name`: Partial role name match (LIKE %pattern%)
- **Returns**:
  - Tuple with JOIN query

### `update(cursor, emp_id: int, update_fields: dict) -> bool`
Modifies employee fields.
- **Parameters**:
  - `emp_id`: Target employee ID
  - `update_fields`: Dictionary of `{field: new_value}`
- **Returns**:
  - `True` if any rows were updated

### `delete(cursor, emp_id: int) -> bool`
Removes an employee permanently.
- **Parameters**:
  - `emp_id`: Employee ID to delete
- **Returns**:
  - `True` if deletion succeeded

### `get_all(cursor) -> tuple`
Retrieves all employees.
- **Returns**:
  - Tuple for full table scan query

## Design Notes
- All methods expect an open database cursor as first parameter (handled by decorator)
- Fetch methods return raw query tuples for standardized processing
- Write operations (`create/update/delete`) use `commit=True` decorator parameter
- Model validation occurs before service layer invocation