something like this
```python
# payroll_routes.py
@payroll_bp.route('/payrolls', methods=['POST'])
def create_payroll():
    data = request.get_json()
    
    # 1. Validate through EmployeeService
    employee = EmployeeService.get_active(data['employee_id'])
    if not employee:
        return {"error": "Invalid employee"}, 400
    
    # 2. Get eligible worklogs
    worklogs = WorkLogService.get_eligible_for_payroll(
        employee.id,
        data['start_date'],
        data['end_date']
    )
    if not worklogs:
        return {"error": "No worklogs found"}, 400
    
    try:
        # 3. Create payroll shell
        payroll = PayrollService.create_payroll(
            employee.id,
            data['start_date'],
            data['end_date']
        )
        
        # 4. Associate and lock worklogs
        if not (
            PayrollWorklogService.create_associations(payroll.id, worklogs) and
            WorkLogService.bulk_lock([w['id'] for w in worklogs])
        ):
            raise Exception("Failed to process worklogs")
        
        # 5. Calculate and finalize
        PayrollService.calculate_totals(payroll.id, worklogs)
        PayrollService.finalize(payroll.id)
        
        return jsonify(payroll.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400

@payroll_bp.route('/payrolls/<int:payroll_id>/worklogs')
def get_payroll_worklogs(payroll_id):
    data = PayrollService.get_payroll_with_worklogs(payroll_id)
    if not data:
        return {"error": "Payroll not found"}, 404
    
    # Using WorkLogService for additional processing
    worklog_details = WorkLogService.get_details([w['id'] for w in data['worklogs']])
    
    return jsonify({
        **data,
        'worklog_details': worklog_details
    })
```

also first validate in routers layer if data is valid too before passing it to services to process