from pathlib import Path

from alembic.config import Config
from pytest import MonkeyPatch
from sqlalchemy import create_engine, inspect

from ai_commerce_engine.config import get_settings
from alembic import command


def test_migrations_upgrade_and_downgrade_clean_database(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    database = tmp_path / "migration-test.db"
    database_url = f"sqlite:///{database.as_posix()}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    get_settings.cache_clear()
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(config, "head")
    tables = set(inspect(create_engine(database_url)).get_table_names())
    assert {"products", "product_versions", "opportunities", "research_entries"} <= tables

    command.downgrade(config, "base")
    assert inspect(create_engine(database_url)).get_table_names() == ["alembic_version"]
    get_settings.cache_clear()
