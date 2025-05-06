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
