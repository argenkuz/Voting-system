class Votes:
    def __init__(self, username, election_name, candidate_id):
        self.__username = username
        self.__election_name = election_name
        self.__candidate_id = candidate_id


    def get_username(self):
        return self.__username
    def set_username(self, username):
        self.__username = username

    def get_candidate_id(self):
        return self.__candidate_id
    def set_candidate_id(self, candidate_id):
        self.__candidate_id = candidate_id

    def get_election_name(self):
        return self.__election_name
    def set_election_name(self, election_id):
        self.__election_name = election_id


