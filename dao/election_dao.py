from dao.BaseDao import Dao
import sys

sys.path.append("/Users/argenkulzhanov/Desktop/Designer/nursezim/classes")
from election import Election

class ElectionDAO(Dao):
    def __init__(self, db_path):
        super().__init__(db_path)

    def insert(self, election: Election):
        query = "INSERT INTO Elections (name, start_date, end_date) VALUES (?, ?, ?)"
        self.execute_query(query, (election.get_name(), election.get_start_date(), election.get_end_date()))
        self._connection.commit()
        return self._cursor.lastrowid

    def find_by_name(self, name: str):
        query = "SELECT * FROM Elections WHERE name = ?"
        result = self.execute_query(query, (name,)).fetchone()
        if result:
            return Election(result[1], result[2],result[3])
        return None

    def get_all_elections(self):
        query = "SELECT * FROM Elections"
        self._cursor.execute(query)
        return self._cursor.fetchall()