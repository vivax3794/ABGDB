import postgres
from typing import Any

from loguru import logger

from ..config import config


class Database:
    def connect_to_database(self) -> None:
        """
        Create a New Database.
        """

        logger.info("connecting to database")
        self.db = postgres.Postgres(config.database)

        logger.info("creating missing tabels")
        self.db.run(
            """
            CREATE TABLE IF NOT EXISTS settings (
                server_id BIGINT PRIMARY KEY,
                prefix text,
                modlog BIGINT
            )
        """
        )

    def add_server(self, server_id: int) -> None:
        logger.debug(f"adding settings for server {server_id}")

        self.db.run(
            """
            INSERT INTO settings (server_id, prefix, modlog) VALUES (%(id)s, '!', 0)
        """,
            {"id": server_id},
        )

    def update_setting(self, server_id: int, setting: str, new_value: Any) -> None:
        logger.debug(f"updating {setting} for server {server_id} to '{new_value}'")

        self.db.run(
            f"""
            UPDATE settings
            SET {setting} = %(value)s
            WHERE server_id = %(id)s
        """,
            {"value": new_value, "id": server_id},
        )

    def get_setting(self, setting: str, server_id: int) -> Any:
        logger.debug(f"getting {setting} for server {server_id}")
        value = self.db.one(
            f"""
            SELECT {setting}
            FROM settings
            WHERE server_id = %(id)s
        """,
            {"id": server_id},
        )

        return value

    def ensoure_in_db(self, server_id: int) -> None:
        value = self.get_setting("prefix", server_id)
        if value is None:
            self.add_server(server_id)

    def add_field(self, setting: str, type_: str) -> None:
        logger.info(f"adding field {setting} to db")
        self.db.run(f"""
            ALTER TABLE settings
            ADD {setting} {type_}
        """)
