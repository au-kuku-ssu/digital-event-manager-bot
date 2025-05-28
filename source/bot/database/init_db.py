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
        return None  # Return None on failure
    default_university_id = uni_row[0]

    JURY_PEOPLE = {
        "sv": {
            "role": "chair",
            "first_name": "Сергей",
            "last_name": "Миронов",
            "email": "sergey.mironov@gmail.com",
            "tg_name": "smironov",
        },
        "herman_key": {
            "role": "jury",
            "first_name": "Герман",
            "last_name": "Наркайтис",
            "email": "herman.narakaitis@gmail.com",
            "tg_name": "hnarakaitis",
        },
        "alexander_key": {
            "role": "jury",
            "first_name": "Александр",
            "last_name": "Сергеев",
            "email": "alexander.sergeev@gmail.com",
            "tg_name": "asergeev",
        },
        "daria_key": {
            "role": "jury",
            "first_name": "Дарья",
            "last_name": "Сергеева",
            "email": "daria.sergeeva@gmail.com",
            "tg_name": "dsergeeva",
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
            return None  # Return None on failure
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
    return default_university_id  # Return the ID


def _seed_participants_and_dependencies(
    cursor: sqlite3.Cursor, conn: sqlite3.Connection, default_university_id: int
):
    logging.info("Seeding participant dependencies and participants...")

    # 1. Seed People for Participants (if they don't exist)
    participant_people_data = [
        {
            "first_name": "Александр",
            "last_name": "Петров",
            "email": "a.petrov@student.university.edu",
            "tg_name": "alex_petrov",
        },
        {
            "first_name": "Михаил",
            "last_name": "Морозов",
            "email": "m.morozov@student.university.edu",
            "tg_name": "mikhail_m",
        },
        {
            "first_name": "Владимир",
            "last_name": "Лебедев",
            "email": "v.lebedev@student.university.edu",
            "tg_name": "vladimir_leb",
        },
        {
            "first_name": "Ольга",
            "last_name": "Новикова",
            "email": "o.novikova@student.university.edu",
            "tg_name": "olga_nov",
        },
        {
            "first_name": "Юлия",
            "last_name": "Соколова",
            "email": "y.sokolova@student.university.edu",
            "tg_name": "julia_sokol",
        },
        {
            "first_name": "Сергей",
            "last_name": "Романов",
            "email": "s.romanov@student.university.edu",
            "tg_name": "sergey_rom",
        },
    ]

    participant_person_ids = []
    for pp_data in participant_people_data:
        cursor.execute(
            "INSERT OR IGNORE INTO people (first_name, last_name, email, tg_name) VALUES (?, ?, ?, ?)",
            (
                pp_data["first_name"],
                pp_data["last_name"],
                pp_data["email"],
                pp_data["tg_name"],
            ),
        )
        # Fetch the id of the inserted or existing person
        cursor.execute("SELECT id FROM people WHERE email = ?", (pp_data["email"],))
        person_row = cursor.fetchone()
        if person_row:
            participant_person_ids.append(person_row[0])
        else:
            logging.error(f"Could not create or find person {pp_data['email']}")
            conn.rollback()
            return False  # Indicate failure

    # 2. Seed default dependent entities
    # Faculties (depends on Universities)
    cursor.execute(
        "INSERT OR IGNORE INTO faculties (university_id, name) VALUES (?, ?)",
        (default_university_id, "Default Faculty"),
    )
    cursor.execute(
        "SELECT id FROM faculties WHERE name = 'Default Faculty' AND university_id = ?",
        (default_university_id,),
    )
    faculty_row = cursor.fetchone()
    default_faculty_id = faculty_row[0] if faculty_row else None

    # Courses
    cursor.execute("INSERT OR IGNORE INTO courses (year) VALUES (?)", (1,))
    cursor.execute("SELECT id FROM courses WHERE year = 1")
    course_row = cursor.fetchone()
    default_course_id = course_row[0] if course_row else None

    # Departments (needed for Teachers)
    cursor.execute(
        "INSERT OR IGNORE INTO departments (name) VALUES (?)", ("Default Department",)
    )
    cursor.execute("SELECT id FROM departments WHERE name = 'Default Department'")
    department_row = cursor.fetchone()
    default_department_id = department_row[0] if department_row else None

    # Teachers (depends on Universities, Departments, People)
    # For simplicity, let's create one default teacher person record if not exists
    default_teacher_person_email = "teacher@example.com"
    cursor.execute(
        "INSERT OR IGNORE INTO people (first_name, last_name, email, tg_name) VALUES (?, ?, ?, ?)",
        ("Default", "Teacher", default_teacher_person_email, "default_teacher_tg"),
    )
    cursor.execute(
        "SELECT id FROM people WHERE email = ?", (default_teacher_person_email,)
    )
    teacher_person_row = cursor.fetchone()
    default_teacher_person_id = teacher_person_row[0] if teacher_person_row else None

    if not all(
        [
            default_faculty_id,
            default_course_id,
            default_department_id,
            default_teacher_person_id,
        ]
    ):
        logging.error(
            "Failed to create default dependency rows for participants (faculty, course, department, or teacher person)."
        )
        conn.rollback()
        return False

    cursor.execute(
        "INSERT OR IGNORE INTO teachers (university_id, department_id, person_id) VALUES (?, ?, ?)",
        (default_university_id, default_department_id, default_teacher_person_id),
    )
    cursor.execute(
        "SELECT id FROM teachers WHERE university_id = ? AND department_id = ? AND person_id = ?",
        (default_university_id, default_department_id, default_teacher_person_id),
    )
    teacher_row = cursor.fetchone()
    default_teacher_id = teacher_row[0] if teacher_row else None

    # Sections
    cursor.execute(
        "INSERT OR IGNORE INTO sections (name, lecture_hall, time) VALUES (?, ?, ?)",
        ("Default Section", "Hall A", "10:00"),
    )
    cursor.execute("SELECT id FROM sections WHERE name = 'Default Section'")
    section_row = cursor.fetchone()
    default_section_id = section_row[0] if section_row else None

    # Textbook Levels
    cursor.execute(
        "INSERT OR IGNORE INTO textbook_levels (level_abbreviation) VALUES (?)", ("B1",)
    )
    cursor.execute("SELECT id FROM textbook_levels WHERE level_abbreviation = 'B1'")
    level_row = cursor.fetchone()
    default_textbook_level_id = level_row[0] if level_row else None

    if not all([default_teacher_id, default_section_id, default_textbook_level_id]):
        logging.error(
            "Failed to create default dependency rows for participants (teacher, section, or textbook level)."
        )
        conn.rollback()
        return False

    # 3. Seed Participants with explicit IDs 1-11
    # This matches PLACEHOLDER_PRESENTS
    for i in range(len(participant_person_ids)):
        participant_id_to_insert = i
        person_id_for_participant = participant_person_ids[
            i - 1
        ]  # Get corresponding person_id

        # Check if participant with this ID already exists
        cursor.execute(
            "SELECT id FROM participants WHERE id = ?", (participant_id_to_insert,)
        )
        existing_participant = cursor.fetchone()

        if not existing_participant:
            try:
                cursor.execute(
                    """INSERT INTO participants (
                        id, faculty_id, course_id, teacher_id, section_id, person_id,
                        is_poster_participant, is_translators_participate, has_translator_education,
                        textbook_level_id, is_group_leader, presentation_topic,
                        is_notification_allowed, password
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        participant_id_to_insert,
                        default_faculty_id,
                        default_course_id,
                        default_teacher_id,
                        default_section_id,
                        person_id_for_participant,
                        0,
                        0,
                        0,  # Booleans: is_poster_participant, is_translators_participate, has_translator_education
                        default_textbook_level_id,
                        0,  # is_group_leader
                        f"Placeholder Topic for ID {participant_id_to_insert}",  # presentation_topic
                        1,
                        "password123",  # is_notification_allowed, password
                    ),
                )
            except sqlite3.IntegrityError as e:
                logging.error(
                    f"Integrity error while inserting participant ID {participant_id_to_insert}: {e}. This might happen if IDs are not unique or FK constraints fail despite checks."
                )
                conn.rollback()
                return False
        else:
            logging.info(
                f"Participant with ID {participant_id_to_insert} already exists. Skipping."
            )

    conn.commit()
    logging.info("Participant dependencies and participants seeding complete.")
    return True


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
                default_university_id_from_seed = _seed_data(cursor, conn)
                if not default_university_id_from_seed:
                    logging.error(
                        "Failed to seed base data (e.g., university). Aborting further seeding."
                    )
                    conn.rollback()
                    return DB_PATH

                if not _seed_participants_and_dependencies(
                    cursor, conn, default_university_id_from_seed
                ):
                    logging.error(
                        "Failed to seed participant data. Rolling back all seeding."
                    )
                    conn.rollback()
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
