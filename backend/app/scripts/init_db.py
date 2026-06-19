from app.database.migrations import upgrade_database

if __name__ == "__main__":
    upgrade_database()
    print("Base de datos actualizada a la última migración.")
