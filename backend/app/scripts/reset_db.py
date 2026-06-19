from app.database.migrations import reset_database

if __name__ == "__main__":
    reset_database()
    print("Base de datos recreada mediante Alembic.")
