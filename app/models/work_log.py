from datetime import datetime

class WorkLog:
    def __init__(self, id: int, date_worked: datetime, hours_worked: float, employee_id: int):
        self.id = id                        # pk, int
        self.date_worked = date_worked      # datetime
        self.hours_worked = hours_worked    # decimal(4, 2)
        self.employee_id = employee_id      # fk, int

    def to_dict(self):
        return {
            "id": self.id,
            "date_worked": self.date_worked,
            "hours_worked": self.hours_worked,
            "employee_id": self.employee_id,
        }