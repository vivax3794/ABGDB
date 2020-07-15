import sqlite3

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

        c.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                server_id INTEGER PRIMARY KEY,
                prefix text
            )
        ''')

        self.conn.commit()

    def add_server(self, server_id: int) -> None:
        logger.debug(f"adding settings for server {server_id}")

        c = self.conn.cursor()
        c.execute('''
            INSERT INTO settings (server_id, prefix) VALUES (?, ?)
        ''', (server_id, "!"))

        self.conn.commit()

    def prefix_update(self, server_id: int, prefix: str) -> None:
        logger.debug(f"updating prefix for server {server_id} to '{prefix}'")

        c = self.conn.cursor()
        c.execute('''
            UPDATE settings
            SET prefix = ?
            WHERE server_id = ?
        ''', (prefix, server_id))

        self.conn.commit()

    def prefix_get(self, server_id: int) -> str:
        logger.debug(f"getting prefix for server {server_id}")

        c = self.conn.cursor()
        c.execute('''
            SELECT prefix
            FROM settings
            WHERE server_id = ?
        ''', (server_id, ))

        return c.fetchone()[0]  # type: ignore
