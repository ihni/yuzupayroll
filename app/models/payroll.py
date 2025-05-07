from datetime import datetime

class Payroll:
    def __init__(self, id: int, pay_period_start: 
                 datetime, pay_period_end: datetime, gross_pay: float, 
                 total_hours: float, employee_id: int):
        self.id = id                                # pk, int
        self.pay_period_start = pay_period_start    # datetime
        self.pay_period_end = pay_period_end        # datetime
        self.gross_pay = gross_pay                  # decimal(10, 2)
        self.total_hours = total_hours              # decimal(5, 2)
        self.employee_id = employee_id              # fk, int

    def to_dict(self):
        return {
            "id": self.id,
            "pay_period_start": self.pay_period_start,
            "pay_period_end": self.pay_period_end,
            "gross_pay": self.gross_pay,
            "total_hours": self.total_hours,
            "employee_id": self.employee_id
        }