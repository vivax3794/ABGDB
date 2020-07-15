import pytest

from src.database import get_database


@pytest.fixture()
def db(tmp_path):
    db_path = tmp_path / "Database.db"
    database = get_database(db_path)

    return database
