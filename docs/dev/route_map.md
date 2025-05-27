# Route Map Documentation

---

## employees

### GET /employees/
- **Description:** Returns a list of all employees.
- **Input:** None
- **Output (context variables):**
    - `employees` (List of Employee objects)
        - `employee.id` (Integer)
        - `employee.first_name` (String)
        - `employee.last_name` (String)
        - `employee.email` (String)
        - `employee.status` (Enum: ACTIVE, INACTIVE, ARCHIVED)
        - `employee.archived_at` (DateTime or None)
        - `employee.created_at` (DateTime)
        - `employee.updated_at` (DateTime)
        - `employee.role` (Role object)
            - `role.id` (Integer)
            - `role.name` (String)
            - `role.rate` (Decimal or Float)
            - `role.status` (Enum: ACTIVE, INACTIVE, ARCHIVED)

### GET /employees/<int:employee_id>
- **Description:** View details of a specific employee.
- **Input:** URL parameter `employee_id` (Integer)
- **Output (context variables):**
    - `employee` (Employee object, same attributes as above)

### POST /employees/create
- **Description:** Creates a new employee.
- **Input (form data):**
    - `first_name` (String)
    - `last_name` (String)
    - `email` (String, unique)
    - `role_id` (Integer, must correspond to an existing role)
    - `status` (Enum string, optional, defaults to ACTIVE)
- **Output:** Redirect or render with errors

### POST /employees/<int:employee_id>/edit
- **Description:** Updates an existing employee by `employee_id`.
- **Input (form data):**
    - `first_name` (String)
    - `last_name` (String)
    - `email` (String)
    - `role_id` (Integer)
    - `status` (Enum string)
- **Output:** Redirect or render with errors

### POST /employees/<int:employee_id>/archive
- **Description:** Archives the employee (sets status to ARCHIVED and sets archived_at).
- **Input:** None
- **Output:** Redirect or flash message

### POST /employees/<int:employee_id>/restore
- **Description:** Restores an archived employee (sets status back to ACTIVE).
- **Input:** None
- **Output:** Redirect or flash message

---

## roles

### GET /roles/
- **Description:** Returns a list of all roles.
- **Input:** None
- **Output (context variables):**
    - `roles` (List of Role objects)
        - `role.id` (Integer)
        - `role.name` (String)
        - `role.rate` (Decimal)
        - `role.status` (Enum: ACTIVE, ARCHIVED)
        - `role.archived_at` (DateTime or None)
        - `role.created_at` (DateTime)
        - `role.updated_at` (DateTime)
        - `role.employees` (List of Employee objects linked to this role)

### GET /roles/<int:role_id>
- **Description:** View details of a specific role.
- **Input:** URL parameter `role_id` (Integer)
- **Output (context variables):**
    - `role` (Role object, same attributes as above)

### POST /roles/create
- **Description:** Creates a new role.
- **Input (form data):**
    - `name` (String, unique)
    - `rate` (Decimal)
- **Output:** Redirect or render with errors

### POST /roles/<int:role_id>/edit
- **Description:** Updates an existing role by `role_id`.
- **Input (form data):**
    - `name` (String)
    - `rate` (Decimal)
    - `status` (Enum string, ACTIVE or ARCHIVED)
- **Output:** Redirect or render with errors

### POST /roles/<int:role_id>/archive
- **Description:** Archives the role (sets status to ARCHIVED and sets archived_at).
- **Input:** None
- **Output:** Redirect or flash message

### POST /roles/<int:role_id>/restore
- **Description:** Restores an archived role (sets status back to ACTIVE).
- **Input:** None
- **Output:** Redirect or flash message

---

## worklogs

### GET /worklogs/
- **Description:** Returns a list of all worklogs.
- **Input:** Optional query parameter:
    - `status` (string enum: ACTIVE, LOCKED, ARCHIVED)
- **Output (context variables):**
    - `worklogs` (List of Worklog objects)
        - `worklog.id` (Integer)
        - `worklog.date` (DateTime)
        - `worklog.hours_worked` (Decimal)
        - `worklog.employee_id` (Integer)
        - `worklog.status` (Enum string)
        - `worklog.archived_at` (DateTime or None)
        - `worklog.locked_at` (DateTime or None)
        - `worklog.created_at` (DateTime)
        - `worklog.updated_at` (DateTime)
        - `worklog.employee` (Employee object linked to this worklog)

### GET /worklogs/eligible
- **Description:** Returns worklogs eligible for inclusion in a payroll for a given employee and date range.
- **Input (query parameters):**
    - `employee_id` (Integer, required)
    - `start_date` (String, YYYY-MM-DD, required)
    - `end_date` (String, YYYY-MM-DD, required)
    - `payroll_id` (Integer, optional)
- **Output (context variables):**
    - `worklogs` (List of eligible Worklog objects matching criteria)
    - `payroll_id` (Integer or None)
    - `start_date` (Date)
    - `end_date` (Date)

### POST /worklogs/<int:worklog_id>/lock
- **Description:** Locks a specific worklog, preventing further edits.
- **Input:** None
- **Output:** Redirect with success/error flash message

### POST /worklogs/<int:worklog_id>/unlock
- **Description:** Unlocks a specific worklog, allowing edits.
- **Input:** None
- **Output:** Redirect with success/error flash message

### POST /worklogs/bulk-lock
- **Description:** Locks multiple worklogs at once.
- **Input (form data):**
    - `worklog_ids` (List of integers)
- **Output:** Redirect with success/error flash message

---

## payrolls

### GET /payrolls/
- **Description:** Returns a list of all payroll records.
- **Input:** None
- **Output (context variables):**
    - `payrolls` (List of Payroll objects)
        - `payroll.id`
        - `payroll.employee_id`
        - `payroll.start_date`
        - `payroll.end_date`
        - `payroll.gross_pay`
        - `payroll.net_pay`
        - `payroll.status` (Enum: DRAFT, FINALIZED, ARCHIVED)
        - `payroll.archived_at` (DateTime or None)
        - `payroll.finalized_at` (DateTime or None)
        - `payroll.created_at`
        - `payroll.updated_at`
        - `payroll.employee` (Employee object)
        - `payroll.payroll_worklogs` (List of PayrollWorklog objects)

### GET /payrolls/<int:payroll_id>
- **Description:** View details of a specific payroll record by `payroll_id`.
- **Input:** URL param `payroll_id`
- **Output (context variables):**
    - `payroll` (Payroll object)
        - All fields as above
        - Includes related `payroll_worklogs`

### POST /payrolls/create
- **Description:** Creates a new payroll record.
- **Input (form data):**
    - `employee_id` (Integer)
    - `start_date` (DateTime string)
    - `end_date` (DateTime string)
    - `gross_pay` (Decimal)
    - `net_pay` (Decimal)
    - Optional: `status` (Enum string)
- **Output:** Redirect with success/error message

### POST /payrolls/<int:payroll_id>/finalize
- **Description:** Finalizes a payroll, locking it and related worklogs.
- **Input:** URL param `payroll_id`
- **Output:** Redirect with success/error message

---