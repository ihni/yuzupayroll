# route map
- a list of routes, methods, and descriptions
- provides a high-level overview of the routes such as
    - route url
    - http method/s
    - input and output data expected

## employees

### GET /employees
- **description**: returns a list of all employees
- **context variables passed**:
    - `employees: List[Employee]`
        - `employee.first_name`
        - `employee.last_name`
        - `employee.email`
        - `employee.created_at`
        - `employee.updated_at`
        - `employee.role` - foreign key to roles table accessing it's attributes using `.` operator on role:
            - `employee.role.name`
            - `employee.role.hourly_rate`