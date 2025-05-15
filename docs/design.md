# System Design Overview

## Purpose
This is a payroll management system for handling employee work logs, payroll generation, and organization-level budgeting.

## Entities
- **Employee**: Holds basic info, role reference.
- **Role**: Contains salary rate info.
- **WorkLog**: Time-in/out per employee, feeds into payroll.
- **Payroll**: Generated summaries per employee.
- **Organization**: Config table for budget cycle.

## Architecture
- Backend: Python (Flask)
- DB: MySQL 8 (via Podman)
- ORM: SQLAlchemy (via Flask Migrate)
