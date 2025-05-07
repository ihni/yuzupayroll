class Employee:
    def __init__(self, id: int, first_name: str, last_name: str, email: str, role_id: int):
        self.id = id                    # pk, int
        self.first_name = first_name    # varchar(45)
        self.last_name = last_name      # varchar(45)
        self.email = email              # varchar(45), unique
        self.role_id = role_id          # fk, int
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role_id": self.role_id
        }