# Overview on Project Structure

## Architecture
- Backend: Python (Flask)
- DB: MySQL 8 (via Podman)
- ORM: SQLAlchemy (via Flask Migrate)

## Schema and ERD
<div align="center">
    <img src="erd.png" alt="ERD">
</div>

## Data lifecycle

> [!NOTE]
> Current design is not set and is constantly being revised

Yuzu proccesses payrolls by compiling employee work logs and finalizing them into an 
The process of generating a payroll slip is through compiling work logs and finalizing it such that it becomes a locked snapshot:
Work logs are used to keep track of when an employee works and for how many hours, these are then used by the payroll via a join table which keeps track of it(`payroll_worklogs`)
Payrolls itsef simply contain the information proccessed from those work logs and are mutable(the information will be regenerated according to the work logs) up until the work logs are locked allowing it to be finalized and immutable. Once locked, the payroll worklogs table will also tick a boolean flag (snapshot_locked) allowing it to leave an audit trail and preventing deletions nor updates to it. Work logs also become immutable at the time of a payroll becoming locked

proccess ->
generate work logs -> (you can either lock the work logs making them immutable or skip this and do it before finalizng the payroll)
-> generate a shell for payroll -> select work logs via date range -> (make any edits while payroll is in draft) -> finalize and lock payroll

Current security concerns with this proccess
TBA