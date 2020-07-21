import sqlite3
from typing import Any

from loguru import logger


class Database:
    conn: sqlite3.Connection

    def connect_to_database(self, file_name: str) -> None:
        """
        Create a New Database.
        """

        logger.info("connecting to database")
        self.conn = sqlite3.connect(file_name)

        logger.info("creating missing tabels")
        c = self.conn.cursor()

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                server_id INTEGER PRIMARY KEY,
                prefix text
            )
        """
        )

        self.conn.commit()

    def add_server(self, server_id: int) -> None:
        logger.debug(f"adding settings for server {server_id}")

        c = self.conn.cursor()
        c.execute(
            """
            INSERT INTO settings (server_id, prefix) VALUES (?, ?)
        """,
            (server_id, "!"),
        )

        self.conn.commit()

    def update_setting(self, server_id: int, setting: str, new_value: Any) -> None:
        logger.debug(f"updating {setting} for server {server_id} to '{new_value}'")

        c = self.conn.cursor()
        c.execute(
            """
            UPDATE settings
            SET ? = ?
            WHERE server_id = ?
        """,
            (setting, new_value, server_id),
        )

        self.conn.commit()

    def get_settting(self, setting: str, server_id: int) -> Any:
        logger.debug(f"getting {setting} for server {server_id}")
        c = self.conn.cursor()
        c.execute(
            """
            SELECT ?
            FROM settings
            WHERE server_id = ?
        """,
            (setting, server_id),
        )

        return c.fetchone()[0]  # type: ignore
