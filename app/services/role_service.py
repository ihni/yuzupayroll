from .. import db
from mysql.connector import Error as MySQLError
from ..models import Role
from ..utils import get_logger

logger = get_logger(__name__)

class RoleService:
    @staticmethod
    def create(role: Role):
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor()

        query = """
            INSERT INTO roles (name, hourly_wage)
            VALUES
            (%(name)s, %(hourly_wage)s)
        """

        try:
            cursor.execute(query, role.to_dict())
            cnx.commit()
            logger.info("Role (%s) created with ID: %s", role.name, cursor.lastrowid)
            return cursor.lastrowid
        except MySQLError as err:
            cnx.rollback()
            logger.error("Failed to create Role: %s", err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(role_id: int) -> Role:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from roles
            WHERE id = %s
        """

        try:
            cursor.execute(query, (role_id,))
            row = cursor.fetchone()
            logger.info("Fetched role id (%s), returning results.", role_id)
            return Role(**row) if row else None
        except MySQLError as err:
            logger.error("Failed to fetch role id (%s): %s", role_id, err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_name(role_name: str) -> Role:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from roles
            WHERE name = %s
        """

        try:
            cursor.execute(query, (role_name,))
            row = cursor.fetchone()
            logger.info("Fetched role name (%s), returning results.", role_name)
            return Role(**row) if row else None
        except MySQLError as err:
            logger.error("Failed to fetch role name (%s): %s", role_name, err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_hourly_rate(hourly_rate: float) -> list[Role]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from roles
            WHERE hourly_rate = %s
        """

        try:
            cursor.execute(query, (hourly_rate,))
            rows = cursor.fetchall()
            logger.info("Fetched all roles with hourly wage of (%s), returning results.", hourly_rate)
            return [Role(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch roles with hourly wage of (%s): %s", hourly_rate, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_count_emp_by_role_id(role_id: int) -> int:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return -1
        cursor = cnx.cursor()

        query = """
            SELECT COUNT(*) FROM roles
            INNER JOIN employees ON roles.id = employees.role_id
            WHERE id = %s
        """

        try:
            cursor.execute(query, (role_id,))
            (count,) = cursor.fetchone()
            logger.info("Fetched count of employees by role id (%s), returning results.", role_id)
            return count
        except MySQLError as err:
            logger.error("Failed to fetch count of employees role id (%s): %s", role_id, err)
            return -1
        finally:
            cursor.close()

    @staticmethod
    def update(role_id: int, update_fields: dict) -> bool:
        # nothing to update
        if not update_fields:
            logger.warning("Empty update fields were passed.")
            return False
        
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return False
        cursor = cnx.cursor()

        # fields in the query and the values to set to
        set_clauses = []
        values = []

        for field, value in update_fields.items():
            set_clauses.append(f"{field} = %s")
            values.append(value)

        # where clause
        values.append(role_id)

        query = f"""
            UPDATE roles
            SET {', '.join(set_clauses)}
            WHERE id = %s
        """

        try:
            cursor.execute(query, values)
            cnx.commit()
            logger.info("Executed update on role id (%s), returning results", role_id)
            return cursor.rowcount > 0
        except MySQLError as err:
            cnx.rollback()
            logger.error("Failed to update role id (%s): %s", role_id, err)
            return False
        finally:
            cursor.close()
        
    @staticmethod
    def delete(role_id: int) -> bool:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return False
        cursor = cnx.cursor()

        query = """
            DELETE FROM roles
            WHERE id = %s
        """

        try:
            cursor.execute(query, (role_id,))
            cnx.commit()
            logger.info("Executed deletion on role id (%s), returning results", role_id)
            return cursor.rowcount > 0
        except MySQLError as err:
            logger.error("Failed to delete role id (%s): %s", role_id, err)
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_all() -> list[Role]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT * FROM roles
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            logger.info("Fetched all roles, returning results.")
            return [Role(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch all roles: %s", err)
            return []
        finally:
            cursor.close()