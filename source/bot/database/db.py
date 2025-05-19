import sqlite3
from source.bot.database.init_db import DB_PATH


def add_user_to_db(
    first_name,
    last_name,
    middle_name,
    phone,
    email,
    tg_name,
    title=None,
    degree=None,
    position=None,
    workplace=None,
):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO people (
                first_name, last_name, middle_name, phone, email,
                title, degree, position, workplace, tg_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                first_name,
                last_name,
                middle_name,
                phone,
                email,
                title,
                degree,
                position,
                workplace,
                tg_name,
            ),
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
        return False

    finally:
        conn.close()


def get_user_by_tg_name(tg_name: str) -> dict | None:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM people WHERE tg_name = ?", (tg_name,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        else:
            return None

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

    finally:
        conn.close()


def register_user_from_state(data: dict, tg_name: str) -> bool:
    fio_parts = data.get("fio", "").split()

    if len(fio_parts) == 1:
        last_name = fio_parts[0]
        first_name = ""
        middle_name = None
    elif len(fio_parts) == 2:
        last_name, first_name = fio_parts
        middle_name = None
    else:
        last_name, first_name, *rest = fio_parts
        middle_name = " ".join(rest) if rest else None

    return add_user_to_db(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        phone=data.get("phone"),
        email=data.get("email"),
        tg_name=tg_name,
        title=None,
        degree=None,
        position=None,
        workplace=None,
    )
