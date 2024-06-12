from crud.crud import CRUD


def main():
    crud = CRUD("sample.db")
    crud.create("sample", ["id INTEGER", "name TEXT", "age INTEGER"], [1, "John", 25])
    crud.create("sample", ["id INTEGER", "name TEXT", "age INTEGER"], [2, "Jane", 30])

    print(crud.read("sample", ["id", "name", "age"]))

    crud.update("sample", ["name", "age"], ["Jane", 31], "id = 2")
    print(crud.read("sample", ["id", "name", "age"]))

    crud.delete("sample", "id = 1")
    print(crud.read("sample", ["id", "name", "age"]))


if __name__ == "__main__":
    main()
