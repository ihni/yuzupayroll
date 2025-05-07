# Models

## Purpose
They act as data containers which represent the core tables, each class contains a **to_dict()** to
easily index the data from them

## Main models
- Employee
- Organization
- Payroll
- Role
- WorkLog

## Descriptions
all fields are **NOT NULL** unless specified

### Employee
| fields        | data_type         |
|---------------|-------------------|
| id            | pk, int           |
| first_name    | varchar(45)       |
| last_name     | varchar(45)       |
| email         | uq, varchar(45)   |
| role_id       | fk, int           |

### Organization
the table and model only acts as a single row config and does not really contribute to the
calculation of the payrolls nor has an effect on the employees nor roles
| fields                | data_type         |
|-----------------------|-------------------|
| id                    | pk, int           |
| name                  | varchar(45)       |
| total_salary_budget   | decimal(10, 2)    |
| budget_start_month    | int default 1     |
| budget_start_day      | int default 1     |
| budget_end_month      | int default 12    |
| budget_end_day        | int default 31    |

### Payroll
| fields            | data_type         |
|-------------------|-------------------|
| id                | pk, int           |
| pay_period_start  | datetime          |
| pay_period_end    | datetime          |
| gross_pay         | decimal(10, 2)    |
| total_hours       | decimal(5, 2)     |
| employee_id       | fk, int           |

### Role
| fields        | data_type         |
|---------------|-------------------|
| id            | pk, int           |
| name          | uq, varchar(45)   |
| hourly_wage   | decimal(10, 2)    |

### WorkLog
| fields        | data_type     |
|---------------|---------------|
| id            | pk, int       |
| date_worked   | datetime      |
| hours_worked  | decimal(4, 2) |
| employee_id   | fk, int       |