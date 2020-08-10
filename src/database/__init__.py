from loguru import logger

from .core import Database
from ..config import config


def get_database(data_base_file: str = config.database) -> Database:
    logger.info(f"loading database from {data_base_file}")
    db = Database()
    db.connect_to_database(data_base_file)

    return db
