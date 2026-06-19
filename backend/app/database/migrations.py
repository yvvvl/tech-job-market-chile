from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import text

from app.database.session import engine

BACKEND_DIR = Path(__file__).resolve().parents[2]


def get_alembic_config() -> Config:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.set_main_option(
        "script_location",
        str(BACKEND_DIR / "alembic"),
    )
    return config


def upgrade_database(revision: str = "head") -> None:
    command.upgrade(get_alembic_config(), revision)


def drop_database_schema() -> None:
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))


def reset_database() -> None:
    drop_database_schema()
    upgrade_database()
