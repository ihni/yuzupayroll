# Payroll Service

## Purpose
Provides static functions to access payroll records and interact with the `payroll` table in the  
database. Includes basic CRUD operations and queries by employee, date range, total hours, and gross pay.

## Public functions

### `create(payroll: Payroll)`  
Creates a new payroll record in the database  
- **Parameters**:  
    - `payroll (Payroll):` an instance of a Payroll model to insert data with  
- **Return value**:  
    - the id of the payroll created (`int`) or `None` on failure  
---

### `get_by_id(payroll_id: int)`  
Fetches a single payroll by its ID  
- **Parameters**:  
    - `payroll_id (int):` the id of the payroll to fetch  
- **Return value**:  
    - a `Payroll` object or `None` if no result or error  
---

### `get_by_date_range(start: datetime, end: datetime)`  
Fetches payroll records between a specific date range  
- **Parameters**:  
    - `start (datetime):` the start date of the pay period  
    - `end (datetime):` the end date of the pay period  
- **Return value**:  
    - a list of `Payroll` objects (could be empty)  
---

### `get_by_employee_id(emp_id: int)`  
Fetches all payroll records for a specific employee  
- **Parameters**:  
    - `emp_id (int):` the employee’s ID  
- **Return value**:  
    - a list of `Payroll` objects (could be empty)  
---

### `get_by_total_hours(total_hours: int)`  
Fetches all payroll records with a specific number of total hours worked  
- **Parameters**:  
    - `total_hours (int):` the number of hours worked to filter by  
- **Return value**:  
    - a list of `Payroll` objects (could be empty)  
---

### `get_by_gross_pay(gross_pay: int)`  
Fetches all payroll records with a specific gross pay amount  
- **Parameters**:  
    - `gross_pay (int):` the gross pay to filter by  
- **Return value**:  
    - a list of `Payroll` objects (could be empty)  
---

### `get_all()`  
Fetches all payroll records  
- **Return value**:  
    - a list of `Payroll` objects (could be empty)  
---

### `update(payroll_id: int, update_fields: dict)`  
Updates a payroll record by its ID using a dictionary of update fields  
- **Parameters**:  
    - `payroll_id (int):` the id of the payroll to update  
    - `update_fields (dict):` a dictionary containing {`field` : `value`}  
- **Return value**:  
    - `True` if update was successful or `False` if not  
---

### `delete(payroll_id: int)`  
Permanently deletes a payroll record by its ID  
- **Parameters**:  
    - `payroll_id (int):` the id of the payroll to delete  
- **Return value**:  
    - `True` if deletion was successful or `False` if not