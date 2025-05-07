class Role:
    def __init__(self, id: int, name: str, hourly_wage: float):
        self.id = id                     # pk, int
        self.name = name                # varchar(45)
        self.hourly_wage = hourly_wage  # decimal(10, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "hourly_wage": self.hourly_wage,
        }