# Role Service

## Overview
Manages database operations for the `roles` table and employee role associations. All methods follow the `db_operation` decorator pattern.

## Interface

### `create(cursor, role: Role) -> int`
Creates a new role entry.
- **Parameters**:
  - `role`: Validated Role model instance
- **Returns**:
  - ID of the created role

### `get_by_id(cursor, role_id: int) -> tuple`
Retrieves a role by ID.
- **Parameters**:
  - `role_id`: Role identifier
- **Returns**:
  - Tuple of `(query, params)` for single-record fetch

### `get_by_name(cursor, role_name: str) -> tuple`
Finds a role by exact name match.
- **Parameters**:
  - `role_name`: Case-sensitive role name
- **Returns**:
  - Tuple for name query

### `get_by_hourly_rate(cursor, hourly_rate: float) -> tuple`
Lists roles with specific hourly rate.
- **Parameters**:
  - `hourly_rate`: Exact rate to match
- **Returns**:
  - Tuple for rate-based query

### `get_count_emp_by_role_id(cursor, role_id: int) -> tuple`
Counts employees assigned to a role.
- **Parameters**:
  - `role_id`: Role identifier
- **Returns**:
  - Tuple for count query (`COUNT(*) as count`)

### `update(cursor, role_id: int, update_fields: dict) -> bool`
Modifies role attributes.
- **Parameters**:
  - `role_id`: Target role ID
  - `update_fields`: Dictionary of `{field: new_value}`
- **Returns**:
  - `True` if update succeeded

### `delete(cursor, role_id: int) -> bool`
Removes a role permanently.
- **Parameters**:
  - `role_id`: Role ID to delete
- **Returns**:
  - `True` if deletion succeeded

### `get_all(cursor) -> tuple`
Retrieves all roles.
- **Returns**:
  - Tuple for full table query

## Design Notes
- Hourly rates stored with 2 decimal precision
- Role names are case-sensitive and unique
- Employee count returns scalar value via `COUNT(*)`
- All write operations use `commit=True`