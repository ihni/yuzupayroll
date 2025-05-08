# Tables in the ERD

## Entities
- **organization**
    - contains the name, budget cycle(excluding the year), and total salary budget
    - acts as a single row configuration table
    - my purpose was to add the ability to visually see the salary changes

- **roles**
    - contains the name, and hourly rate
    - seperated it from the employees entity to isolate the wage based on the role

- **employees**
    - contains name, email, and the role(as a foreign key)

- **work_logs**
    - contains the date worked, hours worked, and the employee that worked(as a foreign key)
    - purpose was to keep track of the work done and to seperate it from the finalized payroll

- **payroll**
    - contains the pay period range(selected by the client), the total hours worked, and gross
      pay which is calculated by using the work log table to get the total hours worked by the
      employee between the given range
    - will definitely make use of JOIN operations

## Data Flow
Work Logs -> Payroll Calculator -> Payroll Table

## Tables

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
| hourly_rate   | decimal(10, 2)    |

### WorkLog
| fields        | data_type     |
|---------------|---------------|
| id            | pk, int       |
| date_worked   | datetime      |
| hours_worked  | decimal(4, 2) |
| employee_id   | fk, int       |