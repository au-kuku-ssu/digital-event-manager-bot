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

    async def get_jury_id_by_access_key(self, access_key: str) -> Optional[int]:
        """Fetches the jury id for the given access key."""
        try:
            self.cursor.execute(
                "SELECT id FROM juries WHERE access_key = ?", (access_key,)
            )
            row = self.cursor.fetchone()
            return row[0] if row else None
        except sqlite3.Error as e:
            logger.error(f"SQL error in get_jury_id_by_access_key: {e}")
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

    async def save_score(
        self, jury_id: int, participant_id: int, criterion: str, value: float
    ) -> None:
        """Saves or updates a score for a given criterion."""
        criterion_column = f"{criterion}_criteria"
        try:
            self.cursor.execute(
                "SELECT id FROM jury_scores WHERE jury_id = ? AND participant_id = ?",
                (jury_id, participant_id),
            )
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute(
                    f"UPDATE jury_scores SET {criterion_column} = ? WHERE jury_id = ? AND participant_id = ?",
                    (value, jury_id, participant_id),
                )
            else:
                criteria_columns = [
                    "organization_criteria",
                    "content_criteria",
                    "visuals_criteria",
                    "mechanics_criteria",
                    "delivery_criteria",
                ]
                values_dict = {
                    col: 0.0 for col in criteria_columns
                }  # Initialize with 0.0 for REAL type
                values_dict[criterion_column] = value

                # Ensure comment column is handled if it's NOT NULL without a default in your schema
                # For now, assuming it can be NULL or has a default.
                columns_str = ", ".join(
                    ["jury_id", "participant_id"] + criteria_columns
                )
                placeholders_str = ", ".join(["?"] * (2 + len(criteria_columns)))
                insert_values = [jury_id, participant_id] + [
                    values_dict[col] for col in criteria_columns
                ]

                self.cursor.execute(
                    f"INSERT INTO jury_scores ({columns_str}) VALUES ({placeholders_str})",
                    insert_values,
                )
            self.conn.commit()
            logger.info(
                f"Score saved/updated for jury {jury_id}, participant {participant_id}, criterion {criterion}."
            )
        except sqlite3.Error as e:
            logger.error(f"SQL error in save_score: {e}")
            self.conn.rollback()

    async def get_scores(self, jury_id: int, participant_id: int) -> Optional[dict]:
        """Fetches all scores for a given jury and participant."""
        try:
            self.cursor.execute(
                "SELECT organization_criteria, content_criteria, visuals_criteria, mechanics_criteria, delivery_criteria FROM jury_scores WHERE jury_id = ? AND participant_id = ?",
                (jury_id, participant_id),
            )
            row = self.cursor.fetchone()
            if row:
                criteria_names = [
                    "organization",
                    "content",
                    "visuals",
                    "mechanics",
                    "delivery",
                ]
                # Filter out None values that might come from NULL columns if a score was deleted/not set
                return {
                    name: val
                    for name, val in zip(criteria_names, row)
                    if val is not None
                }
            return None
        except sqlite3.Error as e:
            logger.error(f"SQL error in get_scores: {e}")
            return None

    async def delete_score(
        self, jury_id: int, participant_id: int, criterion: str
    ) -> None:
        """Sets a specific criterion's score to NULL for a given jury and participant."""
        criterion_column = f"{criterion}_criteria"
        try:
            self.cursor.execute(
                f"UPDATE jury_scores SET {criterion_column} = NULL WHERE jury_id = ? AND participant_id = ?",
                (jury_id, participant_id),
            )
            self.conn.commit()
            logger.info(
                f"Score for criterion {criterion} deleted (set to NULL) for jury {jury_id}, participant {participant_id}."
            )
        except sqlite3.Error as e:
            logger.error(f"SQL error in delete_score: {e}")
            self.conn.rollback()

    async def update_comment(
        self, jury_id: int, participant_id: int, comment: str
    ) -> None:
        """Updates the comment for a given jury and participant's score.
        Ensures a row exists before attempting to update the comment.
        """
        try:
            # First, check if the score row exists, as comment is part of jury_scores
            self.cursor.execute(
                "SELECT id FROM jury_scores WHERE jury_id = ? AND participant_id = ?",
                (jury_id, participant_id),
            )
            score_row = self.cursor.fetchone()

            if not score_row:
                # If no scores exist, we can't just update a comment.
                # Option 1: Insert a new row with all scores as NULL/0 and the comment.
                # This might be complex if criteria columns are NOT NULL without defaults.
                # Option 2: Log an error, as a comment usually pertains to existing scores.
                # For now, let's choose Option 2 and log an error.
                # A more robust solution might involve creating an empty score record first if desired.
                logger.warning(
                    f"Attempted to update comment for non-existing score record: jury {jury_id}, participant {participant_id}. Comment not saved."
                )
                # If you want to create a record: You'd need to list all criteria columns,
                # set them to a default (e.g., 0 or NULL if allowed), and then add the comment.
                # Example: INSERT INTO jury_scores (jury_id, participant_id, comment, org_criteria, ...) VALUES (?, ?, ?, 0, ...)
                return  # Or raise an error

            self.cursor.execute(
                "UPDATE jury_scores SET comment = ? WHERE jury_id = ? AND participant_id = ?",
                (comment, jury_id, participant_id),
            )
            self.conn.commit()
            logger.info(
                f"Comment updated for jury {jury_id}, participant {participant_id}."
            )
        except sqlite3.Error as e:
            logger.error(f"SQL error in update_comment: {e}")
            self.conn.rollback()
