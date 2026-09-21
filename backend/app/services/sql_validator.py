def is_sql_safe(sql: str) -> bool:
    """
    Checks whether a generated SQL string is safe to execute:
    must be a read-only SELECT statement, with no dangerous keywords.
    """
    
    cleaned_sql = sql.strip().upper()

    #  list of dangerous keywords to block
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "CREATE", "ALTER", "TRUNCATE"]

    # loop through dangerous_keywords, return False if any appear in cleaned_sql
    for keyword in dangerous_keywords:
        if keyword in cleaned_sql:
            return False

    return cleaned_sql.startswith("SELECT")


if __name__ == "__main__":
    print(is_sql_safe("SELECT * FROM customers WHERE city = 'Kathmandu';"))  # True
    print(is_sql_safe("DROP TABLE customers;"))  # False
    print(is_sql_safe("UPDATE customers SET city = 'Pokhara';"))  # False
    print(is_sql_safe("SELECT * FROM customers; DROP TABLE customers;"))  # False (dangerous keyword present even after a valid start)