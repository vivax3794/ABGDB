import pytest

from src.database import get_database


@pytest.fixture()
def db(tmp_path):
    database = get_database()

    return database
