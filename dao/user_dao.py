from dao.BaseDao import Dao
import sys

sys.path.append("/Users/argenkulzhanov/Desktop/Designer/nursezim/classes")
from user import User

class UserDAO(Dao):
    def __init__(self, db_path):
        super().__init__(db_path)

    def insert(self, user):
        query = "INSERT INTO Users (username, email, password, phone_number) VALUES (?, ?, ?, ?)"
        self._cursor.execute(query, (user.get_username(), user.get_email(), user.get_password(), user.get_phone_number()))
        self._connection.commit()

    def find_by_username(self, username: str):
        query = "SELECT * FROM Users WHERE username = ?"
        self._cursor.execute(query, (username,))
        result = self._cursor.fetchone()
        if result:
            return User(result[1], result[2], result[3], result[4])
        return None

    def find_by_email(self, email: str):
        query = "SELECT * FROM Users WHERE email = ?"
        self._cursor.execute(query, (email,))
        result = self._cursor.fetchone()
        if result:
            return User(result[1], result[2], result[3], result[4])
        return None

    def get_all_users(self):
        query = "SELECT * FROM Users"
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def update_password(self, email: str, new_password: str):
        query = "UPDATE Users SET password = ? WHERE email = ?"
        self.execute_query(query, (new_password, email))
        self._connection.commit()
        return self._cursor.rowcount
