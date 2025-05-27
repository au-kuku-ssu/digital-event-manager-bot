import sqlite3
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "digital_event_manager.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")


def _seed_data(cursor: sqlite3.Cursor, conn: sqlite3.Connection):
    """Seeds initial data into the database."""
    logging.info("Seeding initial jury data...")

    # # 1. Ensure Default University exists
    default_uni_name = "Saratov State University"
    cursor.execute(
        "INSERT OR IGNORE INTO universities (name) VALUES (?)", (default_uni_name,)
    )
    cursor.execute("SELECT id FROM universities WHERE name = ?", (default_uni_name,))
    uni_row = cursor.fetchone()
    if not uni_row:
        logging.error(f"ERROR: Could not create or find {default_uni_name}.")
        conn.rollback()  # Rollback if essential data can't be set up
        return
    default_university_id = uni_row[0]

    JURY_PEOPLE = {
        "bob_key": {
            "role": "jury",
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob.smith@gmail.com",
            "tg_name": "bob_smith",
        },
        "alice_key": {
            "role": "chair",
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@gmail.com",
            "tg_name": "alice_johnson",
        },
        "charlie_key": {
            "role": "jury",
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "charlie.brown@gmail.com",
            "tg_name": "charlie_brown",
        },
    }

    # 2. Ensure Default Person exists for jury members
    # Using a generic person for all placeholder juries as specific person details aren't in PLACEHOLDER_JURY
    for person_access_key, person_details in JURY_PEOPLE.items():
        cursor.execute(
            "INSERT OR IGNORE INTO people (first_name, last_name, email, tg_name) VALUES (?, ?, ?, ?) RETURNING id",
            (
                person_details["first_name"],
                person_details["last_name"],
                person_details["email"],
                person_details["tg_name"],
            ),
        )
        person_row = cursor.fetchone()
        if not person_row:
            logging.error(
                f"ERROR: Could not create or find {person_details['first_name']} {person_details['last_name']}."
            )
            conn.rollback()  # Rollback if essential data can't be set up
            return
        person_id = person_row[0]

        try:
            # Using INSERT OR IGNORE to avoid issues if script is run multiple times
            # and access_key should be unique.
            cursor.execute(
                "INSERT OR IGNORE INTO juries (university_id, person_id, is_chairman, access_key) VALUES (?, ?, ?, ?)",
                (
                    default_university_id,
                    person_id,
                    person_details.get("role") == "chair",
                    person_access_key,
                ),
            )
        except sqlite3.IntegrityError as ie:
            # This might happen if access_key is not unique, though IGNORE should handle it.
            # Or if university_id/person_id constraint fails, which should be caught by earlier checks.
            logging.error(
                f"Could not insert jury with access key {person_id} due to integrity error: {ie}"
            )
        except Exception as e:
            logging.error(f"An error occurred while inserting jury {person_id}: {e}")

    conn.commit()  # Commit all seeding changes
    logging.info("Initial data seeding complete.")


def _display_tables(cursor: sqlite3.Cursor):
    """Displays current tables in the database."""
    logging.info("\nCurrent tables in the database:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        logging.info(f" - {table[0]}")


def init_db() -> str:
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)

    # Check if DB exists. If it does, we assume schema and seeding is done.
    # For more robust seeding, you might need a versioning system or a flag.
    db_exists = os.path.exists(DB_PATH)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            if not db_exists:
                logging.info("Database does not exist. Initializing schema...")
                with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                conn.executescript(sql_script)
                logging.info("The database schema is initialized.")
            else:
                logging.info("Database already exists. Skipping schema initialization.")

            # Seeding data - only if the database was just created
            if not db_exists:
                _seed_data(cursor, conn)
                _display_tables(cursor)

    except sqlite3.OperationalError as e:
        logging.error(f"Error connecting to or operating on the database: {e}")
    except FileNotFoundError:
        logging.error(f"ERROR: Schema file {SCHEMA_FILE} not found.")
    except Exception as e_global:
        logging.error(
            f"An unexpected error occurred during database initialization: {e_global}"
        )

    return DB_PATH


if __name__ == "__main__":
    init_db()
