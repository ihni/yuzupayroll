class Organization:
    def __init__(self, id: int, name: str, total_salary_budget: float,
                 budget_start_month: int, budget_start_day: int,
                 budget_end_month: int, budget_end_day: int):
        self.id = id                                    # int
        self.name = name                                # varchar(45)
        self.total_salary_budget = total_salary_budget  # decimal(10, 2)
        self.budget_start_month = budget_start_month    # int
        self.budget_start_day = budget_start_day        # int
        self.budget_end_month = budget_end_month        # int
        self.budget_end_day = budget_end_day            # int

    def get_budget_range(self):
        return {
            "start": (self.budget_start_month, self.budget_start_day),
            "end": (self.budget_end_month, self.budget_end_day),
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "total_salary_budget": self.total_salary_budget,
            "budget_start_month": self.budget_start_month,
            "budget_start_day": self.budget_start_day,
            "budget_end_month": self.budget_end_month,
            "budget_end_day": self.budget_end_day,
        }