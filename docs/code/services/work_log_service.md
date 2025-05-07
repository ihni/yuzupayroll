# Work Log Service

## Purpose
Provides static functions to access work logs and interact with the `work_logs` table in the  
database. Includes basic CRUD operations and queries by employee, date, and hours worked.

## Public functions

### `create(work_log: WorkLog)`  
Creates a new work log in the database  
- **Parameters**:  
    - `work_log (WorkLog):` an instance of a WorkLog model to insert data with  
- **Return value**:  
    - the id of the work log created (`int`) or `None` on failure  
---

### `get_by_id(work_log_id: int)`  
Fetches a single work log by its ID  
- **Parameters**:  
    - `work_log_id (int):` the id of the work log to fetch  
- **Return value**:  
    - a `WorkLog` object or `None` if no result or error  
---

### `get_by_date(date: datetime)`  
Fetches work logs by the date worked  
- **Parameters**:  
    - `date (datetime):` the specific date to search for logs  
- **Return value**:  
    - a list of `WorkLog` objects (could be empty)  
---

### `get_by_employee_id(emp_id: int)`  
Fetches all work logs for a specific employee  
- **Parameters**:  
    - `emp_id (int):` the employee’s ID  
- **Return value**:  
    - a list of `WorkLog` objects (could be empty)  
---

### `get_by_hour_worked(hours_worked: int)`  
Fetches all work logs with a specific number of hours worked  
- **Parameters**:  
    - `hours_worked (int):` the number of hours to filter by  
- **Return value**:  
    - a list of `WorkLog` objects (could be empty)  
---

### `get_all()`  
Fetches all work logs  
- **Return value**:  
    - a list of `WorkLog` objects (could be empty)  
---

### `update(work_log_id: int, update_fields: dict)`  
Updates a work log entry by its ID using a dictionary of update fields  
- **Parameters**:  
    - `work_log_id (int):` the id of the work log to update  
    - `update_fields (dict):` a dictionary containing {`field` : `value`}  
- **Return value**:  
    - `True` if update was successful or `False` if not  
---

### `delete(work_log_id: int)`  
Permanently deletes a work log by its ID  
- **Parameters**:  
    - `work_log_id (int):` the id of the work log to delete  
- **Return value**:  
    - `True` if deletion was successful or `False` if not  