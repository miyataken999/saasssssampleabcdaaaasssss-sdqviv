import duckdb
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str


def create_database():
    conn = duckdb.connect(database=":memory:")
    return conn


def create_table(conn):
    conn.execute("CREATE TABLE users (id INTEGER, name VARCHAR, email VARCHAR)")


def insert_data(conn, users):
    conn.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", users)


def query_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


def main():
    conn = create_database()
    create_table(conn)

    users = [
        (1, "John Doe", "john@example.com"),
        (2, "Jane Doe", "jane@example.com"),
        (3, "Bob Smith", "bob@example.com"),
    ]

    for user in users:
        insert_data(conn, user)

    results = query_data(conn)
    for row in results:
        print(row)


if __name__ == "__main__":
    main()
