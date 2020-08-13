from loguru import logger

from src.database.core import Database
from src.config import config


def get_database() -> Database:
    db = Database()
    db.connect_to_database()

    return db
