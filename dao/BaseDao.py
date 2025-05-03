import sqlite3
import time

class Dao:
    def __init__(self, db_path):
        self._connection = sqlite3.connect(db_path)
        self._connection.execute("PRAGMA busy_timeout = 5000")  # Устанавливаем время ожидания 5 секунд
        self._cursor = self._connection.cursor()
        self._connection.execute("PRAGMA journal_mode=WAL")  # Включаем WAL для улучшенной работы с блокировками

    def execute_query(self, query, params=None):
        """
        Выполнение запросов, таких как INSERT, UPDATE, DELETE, с коммитом.
        Возвращает курсор для дальнейшей работы.
        """
        attempts = 3
        for attempt in range(attempts):
            try:
                self._cursor.execute(query, params or [])
                self._connection.commit()
                return self._cursor
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower():
                    time.sleep(1)  # Подождать 1 секунду перед повторной попыткой
                else:
                    raise  # Если ошибка не из-за блокировки, пробрасываем ее
        raise sqlite3.OperationalError("Database is still locked after multiple attempts")

    def fetch_all(self, query, params=None):
        """
        Выполнение SELECT-запроса и возврат всех результатов.
        """
        attempts = 3
        for attempt in range(attempts):
            try:
                self._cursor.execute(query, params or [])
                return self._cursor.fetchall()
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower():
                    time.sleep(1)  # Подождать 1 секунду перед повторной попыткой
                else:
                    raise  # Если ошибка не из-за блокировки, пробрасываем ее
        raise sqlite3.OperationalError("Database is still locked after multiple attempts")

    def fetch_one(self, query, params=None):
        """
        Выполнение SELECT-запроса и возврат только одной строки результата.
        """
        attempts = 3
        for attempt in range(attempts):
            try:
                self._cursor.execute(query, params or [])
                return self._cursor.fetchone()
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower():
                    time.sleep(1)  # Подождать 1 секунду перед повторной попыткой
                else:
                    raise  # Если ошибка не из-за блокировки, пробрасываем ее
        raise sqlite3.OperationalError("Database is still locked after multiple attempts")

    def close(self):
        self._cursor.close()
        self._connection.close()
