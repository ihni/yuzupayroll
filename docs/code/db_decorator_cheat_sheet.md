# `db_operation` Decorator Guide
When to Use `cursor.execute()` vs. Automatic Execution
---
## 1. Methods That NEED Manual cursor.execute()
Use when:
    - You need to execute multiple statements in one method
    - You require custom pre/post-processing of results
    - You're calling stored procedures
    - You need special cursor options

```python
@db_operation()  # No fetch/commit params
def complex_operation(cursor):
    # Manual execution required
    cursor.execute("SET @special_var = 1")
    cursor.execute("CALL complex_procedure(%s)", (param,))
    return process_results(cursor.fetchall())
```
---

## 2. Methods That SHOULD NOT Use cursor.execute()

Use when:
    - You're doing simple CRUD operations
    - You only need standard fetch behavior (one/many rows)
    - You want auto-commit for writes

```python
@db_operation(fetch=True)  # Auto-executes and fetches
def get_employee(cursor, emp_id):
    return "SELECT * FROM employees WHERE id = %s", (emp_id,)
    # No execute() needed!
```