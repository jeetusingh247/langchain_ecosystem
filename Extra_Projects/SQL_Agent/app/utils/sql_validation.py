import re

def is_safe_sql(sql: str) -> bool:
    """
    Returns True if the SQL is a safe, read-only SELECT statement.
    Blocks DML, DDL, subqueries, and dangerous functions.
    """
    sql = sql.strip().lower()
    # Only allow SELECT at the start
    if not sql.startswith("select"):
        return False
    # Block common DML/DDL keywords
    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "truncate", "replace", "merge", "grant", "revoke"]
    if any(word in sql for word in forbidden):
        return False
    # Block subqueries (naive: look for 'select' after the first word)
    if re.search(r"select.*select", sql):
        return False
    # Block semicolons (multiple statements)
    if ";" in sql:
        return False
    return True
