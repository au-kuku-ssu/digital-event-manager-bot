import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "digital_event_manager.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")

def init_db():
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)

    if os.path.exists(DB_PATH):
        print("Database already exists, skipping initialization")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                sql_script = f.read()

            conn.executescript(sql_script)
            print("The database is initialized")

            print("\nCurrent tables in the database:")
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                print(f" - {table[0]}")

            print("\nTable structure and data types:")
            for table in tables:
                print(f"\nTable: {table[0]}")
                cursor = conn.execute(f"PRAGMA table_info({table[0]});")
                columns = cursor.fetchall()
                for col in columns:
                    cid, name, datatype, notnull, dflt_value, pk = col
                    print(f"   - {name} ({datatype}) {'PRIMARY KEY' if pk else ''}")

    except sqlite3.OperationalError as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    init_db()
