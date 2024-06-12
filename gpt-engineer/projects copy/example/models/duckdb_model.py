import duckdb


class DuckDBModel:
    def __init__(self, db_file):
        self.conn = duckdb.connect(database=db_file)

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.conn.execute(query)

    def insert(self, table_name, values):
        query = f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in values])})"
        self.conn.execute(query, values)

    def select(self, table_name, columns, conditions=None):
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        return self.conn.execute(query).fetchall()

    def update(self, table_name, columns, values, conditions):
        if not conditions:
            raise ValueError("Conditions are required for update operations.")
        query = f"UPDATE {table_name} SET {', '.join([f'{col} = ?' for col in columns])} WHERE {conditions}"
        self.conn.execute(query, values)

    def delete(self, table_name, conditions):
        if not conditions:
            raise ValueError("Conditions are required for delete operations.")
        query = f"DELETE FROM {table_name} WHERE {conditions}"
        self.conn.execute(query)


# 例としての使用方法
if __name__ == "__main__":
    db = DuckDBModel("test.db")
    db.create_table("users", ["id INTEGER", "name TEXT"])
    db.insert("users", [1, "Alice"])
    print(db.select("users", ["*"]))
    db.update("users", ["name"], ["Alice Smith"], "id = 1")
    print(db.select("users", ["*"]))
    db.delete("users", "id = 1")
    print(db.select("users", ["*"]))
