from ..models import Role
from ..utils import get_logger, db_operation

logger = get_logger(__name__)

class RoleService:

    @staticmethod
    @db_operation(commit=True)
    def create(cursor, role: Role):
        query = """
            INSERT INTO roles (name, hourly_rate)
            VALUES (%(name)s, %(hourly_rate)s)
        """
        cursor.execute(query, role.to_dict_for_insert())
        logger.info("Role created with ID: %s", cursor.lastrowid)
        return cursor.lastrowid

    @staticmethod
    @db_operation(fetch=True)
    def get_by_id(cursor, role_id: int) -> tuple:
        query = "SELECT * from roles WHERE id = %s"
        return query, (role_id,)

    @staticmethod
    @db_operation(fetch=True)
    def get_by_name(cursor, role_name: str) -> tuple:   
        query = "SELECT * from roles WHERE name = %s"
        return query, (role_name,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_hourly_rate(cursor, hourly_rate: float) -> tuple:
        query = "SELECT * from roles WHERE hourly_rate = %s"
        return query, (hourly_rate,)

    @staticmethod
    @db_operation(fetch=True)
    def get_count_emp_by_role_id(cursor, role_id: int) -> tuple:
        query = """
            SELECT COUNT(*) FROM employees
            INNER JOIN roles ON employees.role_id = roles.id
            WHERE roles.id = %s
        """
        return query, (role_id,)

    @staticmethod
    @db_operation(commit=True)
    def update(cursor, role_id: int, update_fields: dict) -> bool:
        if not update_fields:
            logger.warning("Empty update fields were passed.")
            return False
        
        set_clauses = []
        values = []

        for field, value in update_fields.items():
            set_clauses.append(f"{field} = %s")
            values.append(value)
        values.append(role_id)

        query = f"""
            UPDATE roles SET {', '.join(set_clauses)}
            WHERE id = %s
        """

        cursor.execute(query, values)
        return cursor.rowcount > 0
    
    @staticmethod
    @db_operation(commit=True)
    def delete(cursor, role_id: int) -> bool:
        query = "DELETE FROM roles WHERE id = %s"
        cursor.execute(query, (role_id,))
        return cursor.rowcount > 0

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_all(cursor) -> tuple:
        query = "SELECT * FROM roles"
        return query, ()