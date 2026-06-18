from app.database.models import Base
from app.database.session import engine

if __name__ == "__main__":
    print("Tablas detectadas por SQLAlchemy:")
    for table_name in sorted(Base.metadata.tables.keys()):
        print(f" - {table_name}")

    Base.metadata.create_all(bind=engine)

    print("✅ Tablas creadas correctamente.")
