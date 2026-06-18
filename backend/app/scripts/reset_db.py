from app.database.models import Base
from app.database.session import engine

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Base de datos recreada correctamente.")
