from loguru import logger

from .core import Database
from ..config import config


def get_database() -> Database:
    db = Database()
    db.connect_to_database()

    return db
