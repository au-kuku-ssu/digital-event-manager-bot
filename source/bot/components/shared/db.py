import sqlite3
from typing import Optional
import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        logger.info("Database instance created.")

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.cursor = self.conn.cursor()
            logger.info("Database connection successful.")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
        return self

    def disconnect(self):
        if self.conn:
            try:
                self.conn.close()
                logger.info("Database connection closed successfully.")
            except sqlite3.Error as e:
                logger.error(f"Failed to close database connection: {e}")

    async def get_jury_role_by_access_key(self, access_key: str) -> Optional[bool]:
        """Fetches the jury role (is_chairman) for the given access key and returns as bool."""
        try:
            self.cursor.execute(
                "SELECT is_chairman FROM juries WHERE access_key = ?", (access_key,)
            )
            row = self.cursor.fetchone()
            if row:
                return row[0]
            return None  # Key not found
        except sqlite3.Error as e:
            logger.error(f"SQL error in get_jury_role_by_access_key: {e}")
            return None

    async def get_jury_name_by_access_key(self, access_key: str) -> Optional[str]:
        """Fetches the jury name (first_name last_name) for the given access key using a JOIN."""
        try:
            self.cursor.execute(
                """
                SELECT p.first_name, p.last_name 
                FROM people p
                JOIN juries j ON p.id = j.person_id
                WHERE j.access_key = ?
            """,
                (access_key,),
            )
            row = self.cursor.fetchone()
            return f"{row[0]} {row[1]}" if row else None
        except sqlite3.Error as e:
            logger.error(f"SQL error in get_jury_name_by_access_key: {e}")
            return None

    async def get_all_juries_with_names(self) -> list[dict]:
        """Fetches all juries from the database with their names."""
        try:
            self.cursor.execute("""
                SELECT j.access_key, p.first_name, p.last_name
                FROM juries j
                JOIN people p ON j.person_id = p.id
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"SQL error in get_all_juries: {e}")
            return []
