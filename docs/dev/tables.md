# Tables in the ERD

## Entities
- **organization**
    - contains the name, budget cycle(excluding the year), and total salary budget
    - acts as a single row configuration table
    - used for visualizing salary budget changes across time, not tied directly to payroll calculations

- **roles**
    - contains the name, and hourly rate
    - seperated it from the employees entity to isolate the wage based on the role

- **employees**
    - contains personal info (first/last name, email) and a foreign key to the associated role

- **work_logs**
    - logs individual work entries per employee: when they worked and how many hours
    - used as input data for payroll calculation
    - decouples raw work data from finalized payroll records

- **payroll**
    - finalized payroll records generated for a pay period
    - includes pay range, total hours, gross pay and a foreign key to the associated employee

## Data Flow
Work Logs -> Payroll Calculator -> Payroll Table