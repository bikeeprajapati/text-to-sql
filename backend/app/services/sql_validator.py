import re

def is_sql_safe(sql: str) -> bool:
    """
    Checks whether a generated SQL string is safe to execute:
    must be a read-only SELECT statement, with no dangerous keywords.
    """
    cleaned_sql = sql.strip().upper()

    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "CREATE", "ALTER", "TRUNCATE"]

    for keyword in dangerous_keywords:
        # \b = word boundary, so "CREATE" won't match inside "CREATED_AT"
        if re.search(rf"\b{keyword}\b", cleaned_sql):
            return False

    return cleaned_sql.startswith("SELECT")