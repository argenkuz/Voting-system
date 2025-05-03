import sqlite3
import time

class Dao:
    def __init__(self, db_path):
        self._connection = sqlite3.connect(db_path)
        self._connection.execute("PRAGMA busy_timeout = 5000")
        self._cursor = self._connection.cursor()
        self._connection.execute("PRAGMA journal_mode=WAL")

    def execute_query(self, query, params=None):
        attempts = 3
        for attempt in range(attempts):
            try:
                self._cursor.execute(query, params or [])
                self._connection.commit()
                return self._cursor
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower():
                    time.sleep(1)
                else:
                    raise
        raise sqlite3.OperationalError("Database is still locked after multiple attempts")

    def fetch_all(self, query, params=None):
        attempts = 3
        for attempt in range(attempts):
            try:
                self._cursor.execute(query, params or [])
                return self._cursor.fetchall()
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower():
                    time.sleep(1)
                else:
                    raise
        raise sqlite3.OperationalError("Database is still locked after multiple attempts")

    def fetch_one(self, query, params=None):

        attempts = 3
        for attempt in range(attempts):
            try:
                self._cursor.execute(query, params or [])
                return self._cursor.fetchone()
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower():
                    time.sleep(1)
                else:
                    raise
        raise sqlite3.OperationalError("Database is still locked after multiple attempts")

    def close(self):
        self._cursor.close()
        self._connection.close()
