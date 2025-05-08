class Role:
    def __init__(self, name: str, hourly_rate: float, id: int=None):
        self.id = id                     # pk, int
        self.name = name                # varchar(45)
        self.hourly_rate = hourly_rate  # decimal(10, 2)

    def to_dict_for_insert(self):
        return {
            "id": self.id,
            "name": self.name,
            "hourly_rate": self.hourly_rate,
        }

    def to_dict(self):
        return {
            "name": self.name,
            "hourly_rate": self.hourly_rate,
        }