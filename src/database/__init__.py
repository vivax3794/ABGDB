from .core import Database
from config import DATABASE as DEFAULT_DATABASE_FILE


def get_database(data_base_file: str = DEFAULT_DATABASE_FILE) -> Database:
    db = Database()
    db.connect_to_database(data_base_file)

    return db
