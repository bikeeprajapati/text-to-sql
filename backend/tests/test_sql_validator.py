from app.services.sql_validator import is_sql_safe


def test_simple_select_is_safe():
    assert is_sql_safe("SELECT * FROM customers WHERE city = 'Kathmandu';") is True


def test_drop_is_blocked():
    assert is_sql_safe("DROP TABLE customers;") is False


def test_update_is_blocked():
    assert is_sql_safe("UPDATE customers SET city = 'Pokhara';") is False


def test_dangerous_keyword_after_valid_select_is_blocked():
    assert is_sql_safe("SELECT * FROM customers; DROP TABLE customers;") is False


def test_query_not_starting_with_select_is_blocked():
    assert is_sql_safe("customers SELECT * FROM") is False


def test_created_at_column_is_not_mistaken_for_create():
    # Regression test: "CREATE" is a substring of "CREATED_AT".
    # A naive `"CREATE" in sql` check used to reject this valid query.
    sql = "SELECT COUNT(*) FROM customers WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '30 days';"
    assert is_sql_safe(sql) is True


def test_updated_at_column_is_not_mistaken_for_update():
    # Same bug class as above, but for UPDATE / updated_at.
    sql = "SELECT * FROM orders WHERE updated_at >= CURRENT_TIMESTAMP - INTERVAL '7 days';"
    assert is_sql_safe(sql) is True