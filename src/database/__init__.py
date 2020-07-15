from loguru import logger

from .core import Database
from config import DATABASE as DEFAULT_DATABASE_FILE


def get_database(data_base_file: str = DEFAULT_DATABASE_FILE) -> Database:
    logger.info(f"loading database from {data_base_file}")
    db = Database()
    db.connect_to_database(data_base_file)

    return db
