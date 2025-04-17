from sqlalchemy import create_engine, inspect

engine = create_engine("postgresql+psycopg2://davi:123456@localhost:5432/postgres")
inspector = inspect(engine)

schemas = inspector.get_schema_names()
print("Schemas:", schemas)

tables = inspector.get_table_names(schema="northwind")
print("Tabelas no schema 'northwind':", tables)