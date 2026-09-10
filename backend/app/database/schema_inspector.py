from sqlalchemy import inspect
from app.database.connection import engine

inspector = inspect(engine)
tables = inspector.get_table_names()

def get_all_tables_with_columns():
    """
    Get all tables with their columns in the database.

    Returns:
        dict: A dictionary where keys are table names and values are lists of column names.
    """
    tables_with_columns = {}
    for table in tables:
        columns = [column['name'] for column in inspector.get_columns(table)]
        tables_with_columns[table] = columns
    return tables_with_columns

if __name__ == "__main__":
    tables_with_columns = get_all_tables_with_columns()
    for table, columns in tables_with_columns.items():
        print(f"Table: {table}, Columns: {columns}")
