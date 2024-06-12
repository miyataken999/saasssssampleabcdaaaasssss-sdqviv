from models.duckdb_model import DuckDBModel


class CRUD:
    def __init__(self, db_file):
        self.db = DuckDBModel(db_file)

    def create(self, table_name, columns, values):
        self.db.create_table(table_name, columns)
        self.db.insert(table_name, values)

    def read(self, table_name, columns, conditions=None):
        return self.db.select(table_name, columns, conditions)

    def update(self, table_name, columns, values, conditions):
        self.db.update(table_name, columns, values, conditions)

    def delete(self, table_name, conditions):
        self.db.delete(table_name, conditions)
