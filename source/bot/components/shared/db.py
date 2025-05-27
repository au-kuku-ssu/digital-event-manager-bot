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
        self, jury_id: int, participant_id: int, criterion: str, value: float,
        editor_jury_id: Optional[int] = None, is_chair_edit: bool = False
    ) -> None:
        """Saves or updates a score for a given criterion.
           If is_chair_edit is True, logs the change and editor_jury_id must be provided.
        """
        criterion_column = f"{criterion}_criteria"
        jury_scores_row_id = None
        try:
            self.cursor.execute(
                "SELECT id FROM jury_scores WHERE jury_id = ? AND participant_id = ?",
                (jury_id, participant_id),
            )
            row = self.cursor.fetchone()
            if row:
                jury_scores_row_id = row[0]
                self.cursor.execute(
                    f"UPDATE jury_scores SET {criterion_column} = ? WHERE id = ?",
                    (value, jury_scores_row_id),
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
                
                columns_str = ", ".join(["jury_id", "participant_id"] + criteria_columns)
                placeholders_str = ", ".join(["?"] * (2 + len(criteria_columns)))
                insert_values = [jury_id, participant_id] + [
                    values_dict[col] for col in criteria_columns
                ]
                
                self.cursor.execute(
                    f"INSERT INTO jury_scores ({columns_str}) VALUES ({placeholders_str}) RETURNING id",
                    insert_values,
                )
                inserted_row = self.cursor.fetchone()
                if inserted_row:
                    jury_scores_row_id = inserted_row[0]
            
            self.conn.commit()
            logger.info(
                f"Score saved/updated for jury {jury_id}, participant {participant_id}, criterion {criterion}."
            )

            # Log change if it's a chair edit
            if is_chair_edit and editor_jury_id is not None and jury_scores_row_id is not None:
                await self._log_score_change(jury_scores_row_id, editor_jury_id)
            elif is_chair_edit and (editor_jury_id is None or jury_scores_row_id is None):
                logger.warning("Chair edit indicated but editor_jury_id or jury_scores_row_id missing. Change not logged.")

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

    async def _log_score_change(self, jury_scores_row_id: int, chairman_jury_id: int) -> None:
        """Logs a change to a score in the jury_scores_changes table."""
        try:
            self.cursor.execute(
                "INSERT INTO jury_scores_changes (jury_scores_id, jury_id) VALUES (?, ?)",
                (jury_scores_row_id, chairman_jury_id)
            )
            self.conn.commit()
            logger.info(f"Score change logged for jury_scores_id {jury_scores_row_id} by chairman_jury_id {chairman_jury_id}.")
        except sqlite3.Error as e:
            logger.error(f"SQL error in _log_score_change: {e}")
            # Not rolling back here as this is a secondary logging action.
            # The main score save should have already committed or rolled back.
            # However, if this logging is critical, a rollback might be considered, 
            # but it would complicate the atomicity with save_score.

    async def get_presentations_with_scores_and_details(self) -> list[dict]:
        """Fetches all presentations (participants) with their scores, comments, and juror details."""
        presentations_data = []
        try:
            # Step 1: Fetch all participants (presentations) and their primary speaker
            self.cursor.execute(
                """
                SELECT p.id, p.presentation_topic, pe.first_name, pe.last_name 
                FROM participants p
                JOIN people pe ON p.person_id = pe.id
                ORDER BY p.id
                """
            )
            participants = self.cursor.fetchall()

            for participant_id, topic, speaker_first, speaker_last in participants:
                presentation_entry = {
                    "id": participant_id,
                    "topic": topic,
                    "speakers": [f"{speaker_first} {speaker_last}"], # Assuming one speaker for now
                    "jury_evaluations": [],
                    "calculated_final_scores_by_juror": {}, # Temp store for individual final scores
                    "final_score": 0.0, # Overall final score for the presentation
                }

                # Step 2 & 3: Fetch scores, comments, and juror details for this participant
                self.cursor.execute(
                    """
                    SELECT 
                        js.jury_id, ju.access_key, pj.first_name, pj.last_name,
                        js.organization_criteria, js.content_criteria, js.visuals_criteria, 
                        js.mechanics_criteria, js.delivery_criteria, js.comment
                    FROM jury_scores js
                    JOIN juries ju ON js.jury_id = ju.id
                    JOIN people pj ON ju.person_id = pj.id
                    WHERE js.participant_id = ?
                    """,
                    (participant_id,)
                )
                evaluations = self.cursor.fetchall()
                
                criteria_names = ["organization", "content", "visuals", "mechanics", "delivery"]
                total_final_score_sum = 0.0
                num_juror_scores = 0

                for eval_row in evaluations:
                    (jury_id, access_key, jury_first, jury_last,
                     org, content, visuals, mechanics, delivery, comment_text) = eval_row
                    
                    scores = {}
                    current_juror_total = 0
                    raw_scores = [org, content, visuals, mechanics, delivery]

                    for i, crit_name in enumerate(criteria_names):
                        if raw_scores[i] is not None:
                            scores[crit_name] = raw_scores[i]
                            current_juror_total += raw_scores[i]
                    
                    # Store this juror's total (final score for this presentation)
                    presentation_entry["calculated_final_scores_by_juror"][access_key] = current_juror_total
                    total_final_score_sum += current_juror_total
                    if scores: # Count this juror if they provided any scores
                        num_juror_scores +=1

                    presentation_entry["jury_evaluations"].append({
                        "juror_access_key": access_key,
                        "juror_name": f"{jury_first} {jury_last}",
                        "scores": scores, # individual criteria scores
                        "comment": comment_text if comment_text else "",
                        "juror_final_score": current_juror_total # final score by this specific juror
                    })
                
                if num_juror_scores > 0:
                    presentation_entry["final_score"] = round(total_final_score_sum / num_juror_scores, 2)
                else:
                    presentation_entry["final_score"] = "-" # Or 0.0, depending on display preference

                presentations_data.append(presentation_entry)
            
            return presentations_data

        except sqlite3.Error as e:
            logger.error(f"SQL error in get_presentations_with_scores_and_details: {e}")
            return []
