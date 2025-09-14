from sqlalchemy import inspect
from app.db.connection import engine

def get_schema():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    schema = {}
    for table in tables:
        columns = inspector.get_columns(table)
        pk = inspector.get_pk_constraint(table)
        fks = inspector.get_foreign_keys(table)
        schema[table] = {
            "columns": columns,
            "primary_key": pk,
            "foreign_keys": fks
        }
    return schema
