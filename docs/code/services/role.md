# Role Service

## Purpose
Provides static functions to access roles and interact with the `roles` table in the  
database. Includes basic CRUD operations and utility queries by name and wage.

## Public functions

### `create(role: Role)`  
Creates a new role in the database  
- **Parameters**:  
    - `role (Role):` an instance of a role model to insert data with  
- **Return value**:  
    - the id of the role created (`int`) or `None` on failure  
---

### `get_by_id(role_id: int)`  
Fetches a single role by its ID  
- **Parameters**:  
    - `role_id (int):` the id of the role to fetch  
- **Return value**:  
    - a `Role` object or `None` if no result or error  
---

### `get_by_name(role_name: str)`  
Fetches a single role by its name  
- **Parameters**:  
    - `role_name (str):` the name of the role to fetch  
- **Return value**:  
    - a `Role` object or `None` if no result or error  
---

### `get_by_hourly_rate(hourly_wage: float)`  
Fetches roles with a specific hourly wage  
- **Parameters**:  
    - `hourly_rate (float):` the rate value to filter roles by  
- **Return value**:  
    - a list of `Role` objects (could be empty)  
---

### `get_count_emp_by_role_id(role_id: int)`  
Fetches count of employees with a specific role  
- **Parameters**:  
    - `role_id (int):` the role id to filter count of employees by  
- **Return value**:  
    - the number of employees in that role
---

### `get_all()`  
Fetches all roles  
- **Return value**:  
    - a list of `Role` objects (could be empty)  
---

### `update(role_id: int, update_fields: dict)`  
Updates a single role by its ID using a dictionary of update fields  
- **Parameters**:  
    - `role_id (int):` the id of the role to update  
    - `update_fields (dict):` a dictionary containing {`field` : `value`}  
- **Return value**:  
    - `True` if update was successful or `False` if not  
---

### `delete(role_id: int)`  
Permanently deletes a single role by its ID  
- **Parameters**:  
    - `role_id (int):` the id of the role to delete  
- **Return value**:  
    - `True` if deletion was successful or `False` if not  
