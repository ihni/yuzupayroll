# Payroll Service

## Overview
Handles all database operations for the `payroll` table using the `db_operation` decorator pattern. Provides CRUD operations and payroll-specific queries.

## Interface

### `create(cursor, payroll: Payroll) -> int`
Creates a new payroll record.
- **Parameters**:
  - `payroll`: Validated Payroll model instance
- **Returns**:
  - ID of the created payroll record

### `get_by_id(cursor, payroll_id: int) -> tuple`
Retrieves a payroll record by ID.
- **Parameters**:
  - `payroll_id`: Payroll record ID
- **Returns**:
  - Tuple of `(query, params)` for single-record fetch

### `get_by_date_range(cursor, start: datetime, end: datetime) -> tuple`
Finds payroll records within a date range.
- **Parameters**:
  - `start`: Start date (inclusive)
  - `end`: End date (inclusive)
- **Returns**:
  - Tuple for multi-record date range query

### `get_by_employee_id(cursor, emp_id: int) -> tuple`
Lists payroll records for a specific employee.
- **Parameters**:
  - `emp_id`: Employee ID
- **Returns**:
  - Tuple for employee-specific query

### `get_by_total_hours(cursor, total_hours: int) -> tuple`
Finds payroll records matching exact hours worked.
- **Parameters**:
  - `total_hours`: Exact hours to match
- **Returns**:
  - Tuple for hours-based query

### `get_by_gross_pay(cursor, gross_pay: int) -> tuple`
Finds payroll records matching exact gross pay amount.
- **Parameters**:
  - `gross_pay`: Exact gross pay amount
- **Returns**:
  - Tuple for gross pay query

### `update(cursor, payroll_id: int, update_fields: dict) -> bool`
Modifies payroll record fields.
- **Parameters**:
  - `payroll_id`: Target payroll ID
  - `update_fields`: Dictionary of `{field: new_value}`
- **Returns**:
  - `True` if any records were updated

### `delete(cursor, payroll_id: int) -> bool`
Removes a payroll record permanently.
- **Parameters**:
  - `payroll_id`: Payroll ID to delete
- **Returns**:
  - `True` if deletion succeeded

### `get_all(cursor) -> tuple`
Retrieves all payroll records.
- **Returns**:
  - Tuple for full table scan query

## Design Notes
- Uses `commit=True` for all write operations
- Date range queries use `BETWEEN` with inclusive bounds
- All monetary amounts are handled as integers (cents/pence)
- Model validation occurs before service layer invocation