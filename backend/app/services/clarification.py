def format_schema_for_prompt(schema_dict):
    """
    Format a schema dictionary into a string suitable for prompting the LLM.
    """
    formatted_schema = []

    for table_name, columns in schema_dict.items():
        formatted_columns = []

        for column in columns:
            column_text = f"{column['name']} ({column['data_type']})"
            if column.get("is_primary_key"):
                column_text += " [primary key]"
            if not column.get("nullable", True):
                column_text += " [not null]"
            formatted_columns.append(column_text)

        formatted_schema.append(
            f"Table: {table_name}\nColumns: {', '.join(formatted_columns)}"
        )

    return "\n\n".join(formatted_schema).strip()


if __name__ == "__main__":
    test_schema = {
        "customers": [
            {"name": "id", "data_type": "INTEGER", "nullable": False, "is_primary_key": True},
            {"name": "email", "data_type": "VARCHAR", "nullable": False, "is_primary_key": False},
        ]
    }
    print(format_schema_for_prompt(test_schema))