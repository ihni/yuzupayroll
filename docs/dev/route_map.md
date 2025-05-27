# Route Map Documentation

---

## roles

### GET /roles/
- **Description:** Returns a list of all roles.
- **Input:** None
- **Output (context variables):**
    - `roles` (List of Role objects)
        - `role.id`
        - `role.name`
        - `role.hourly_rate`
        - `role.created_at`
        - `role.updated_at`
        - `role.employees` (List of Employee objects belonging to this role)

### POST /roles/create
- **Description:** Creates a new role.
- **Input (form data):**
    - `name` (string)
    - `hourly_rate` (decimal)
- **Output:** Redirect to `/roles/`

### POST /roles/update/<role_id>
- **Description:** Updates an existing role by `role_id`.
- **Input (form data):**
    - `name` (string)
    - `hourly_rate` (decimal)
- **Output:** Redirect to `/roles/`

### POST /roles/delete/<role_id>
- **Description:** Deletes the role with `role_id`.
- **Input:** None
- **Output:** Redirect to `/roles/`

---

## employees

### GET /employees/
- **Description:** Returns a list of all employees.
- **Input:** None
- **Output (context variables):**
    - `employees` (List of Employee objects)
        - `employee.first_name`
        - `employee.last_name`
        - `employee.email`
        - `employee.created_at`
        - `employee.updated_at`
        - `employee.role`
            - `employee.role.name`
            - `employee.role.hourly_rate`