# Employee Service

## Purpose
provides static functions to access employees and interact with the `employees` table in the
database. includes basic CRUD operations

## Public functions

### `create(employee: Employee)`
creates a new employee in the database
- **Parameters**:
    - `employee (Employee):` an instance of an employee model to insert data with
- **Return value**:
    - the id of the employee created (`int`) or `None` on failure

### `get_by_id(emp_id: int)`
fetches a single employee by their ID
- **Parameters**:
    - `emp_id (int):` the id of the employee to fetch
- **Return value**:
    - an `Employee` object or `None` if no result or error

### `get_by_email(emp_email: str)`
fetches a single employee by their email
- **Parameters**:
    - `emp_email (str):` the email of the employee to fetch
- **Return value**:
    - an `Employee` object or `None` if no result or error

### `get_by_role_id(role_id: int)`
fetches employees by their role id
- **Parameters**:
    - `role_id (int):` the role id of the employees to fetch
- **Return value**:
    - a list of `Employee` objects (could be empty)

### `get_all()`
fetches all employees
- **Return value**:
    - a list of `Employee` objects (could be empty)

### `update(emp_id: int, update_fields: dict)`
updates a single employee by their ID using a dictionary of update fields
- **Parameters**:
    - `emp_id (int):` the id of the employee to update
    - `update_fields (dict):` a dictionary containing {`field` : `value`}
- **Return value**:
    - `True` if update was successful or `False` if not

### `delete(emp_id: int)`
permanently deletes a single employee by their ID
- **Parameters**:
    - `emp_id (int):` the id of the employee to delete
- **Return value**:
    - `True` if deletion was successful or `False` if not

