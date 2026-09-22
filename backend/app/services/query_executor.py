from sqlalchemy import text
from app.database.connection import engine


def execute_sql(sql: str) -> list:
    """
    Executes a validated, read-only SQL query and returns the results
    as a list of dicts (one dict per row).
    Returns None if execution fails.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql))

        
            rows = [dict(row._mapping) for row in result]

            return rows
    except Exception as e:
        print(f"Query execution failed: {e}")
        return None


if __name__ == "__main__":
    print(execute_sql("SELECT * FROM customers WHERE city = 'Kathmandu';"))