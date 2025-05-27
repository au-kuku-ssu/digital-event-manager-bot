import sqlite3
from typing import Optional
import sys


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        sys.stdout.write("INFO: database is up\n")

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conn.cursor()
        sys.stdout.write("INFO: database connection success\n")
        return self

    def disconnect(self):
        if self.conn:
            self.conn.close()
            sys.stdout.write("INFO: database connection success\n")
