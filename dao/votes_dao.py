from dao.BaseDao import Dao
import sys

sys.path.append("/Users/argenkulzhanov/Desktop/Designer/nursezim/classes")
from votes import Votes

class VotesDAO(Dao):
    def __init__(self, db_path):
        super().__init__(db_path)

    def insert(self, vote: Votes):
        query = "INSERT INTO Votes (username, election_name, candidate_id, voted_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)"
        self.execute_query(query, (vote.get_username(), vote.get_election_name(), vote.get_candidate_id()))
        self._connection.commit()
        return self._cursor.lastrowid

    def has_already_voted(self, username, election_name):
        query = "SELECT COUNT(*) FROM Votes WHERE username = ? AND election_name = ?"
        result = self.execute_query(query, (username, election_name)).fetchone()

        return result[0] > 0

    def save_vote(self, username, election_name, candidate_id):
        query = "INSERT INTO Votes (username, election_name, candidate_id, voted_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)"
        self.execute_query(query, (username, election_name, candidate_id))
        self._connection.commit()