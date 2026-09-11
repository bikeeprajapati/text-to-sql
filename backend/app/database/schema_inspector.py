from sqlalchemy import inspect
from app.database.connection import engine


def get_database_schema():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    tables_with_columns = {}

    for table in tables:
        columns = []

        pk_constraint = inspector.get_pk_constraint(table)
        primary_key_columns = pk_constraint["constrained_columns"]

        for column in inspector.get_columns(table):
            columns.append({
                "name": column["name"],
                "data_type": str(column["type"]),       
                "nullable": column["nullable"],
                "is_primary_key": column["name"] in primary_key_columns
            })

        tables_with_columns[table] = columns

    return tables_with_columns


if __name__ == "__main__":
    tables_with_columns = get_database_schema()
    for table, columns in tables_with_columns.items():
        print(f"Table: {table}, Columns: {columns}")
