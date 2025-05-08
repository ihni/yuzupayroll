# Work Log Service

## Overview
Manages time tracking records in the `work_logs` table using the `db_operation` decorator pattern. Handles employee work hour tracking and reporting.

## Interface

### `create(cursor, work_log: WorkLog) -> int`
Records a new work log entry.
- **Parameters**:
  - `work_log`: Validated WorkLog model instance
- **Returns**:
  - ID of the created work log

### `get_by_id(cursor, work_log_id: int) -> tuple`
Retrieves a work log by ID.
- **Parameters**:
  - `work_log_id`: Log entry identifier
- **Returns**:
  - Tuple of `(query, params)` for single-record fetch

### `get_by_date(cursor, date: datetime.date) -> tuple`
Finds work logs for a specific date.
- **Parameters**:
  - `date`: Exact date to query
- **Returns**:
  - Tuple for date-specific query

### `get_by_employee_id(cursor, emp_id: int) -> tuple`
Lists work logs for an employee.
- **Parameters**:
  - `emp_id`: Employee identifier
- **Returns**:
  - Tuple for employee-specific query

### `get_by_hours_worked(cursor, hours: float) -> tuple`
Finds logs matching exact hours worked.
- **Parameters**:
  - `hours`: Precise hours logged (2 decimal places)
- **Returns**:
  - Tuple for hours-based query

### `get_by_date_range(cursor, start_date: datetime.date, end_date: datetime.date) -> tuple`
Retrieves logs within a date range.
- **Parameters**:
  - `start_date`: Range start (inclusive)
  - `end_date`: Range end (inclusive)
- **Returns**:
  - Tuple for date range query (ordered chronologically)

### `update(cursor, work_log_id: int, update_fields: dict) -> bool`
Modifies work log details.
- **Parameters**:
  - `work_log_id`: Target log ID
  - `update_fields`: Dictionary of `{field: new_value}`
- **Returns**:
  - `True` if update succeeded

### `delete(cursor, work_log_id: int) -> bool`
Removes a work log permanently.
- **Parameters**:
  - `work_log_id`: Log entry to delete
- **Returns**:
  - `True` if deletion succeeded

### `get_all(cursor) -> tuple`
Retrieves all work logs.
- **Returns**:
  - Tuple for full table query

## Design Notes
- Hours tracked with 2 decimal precision (0.25 hour increments)
- Date ranges are inclusive of both start and end dates
- All write operations use `commit=True`
- Results ordered by date when applicable