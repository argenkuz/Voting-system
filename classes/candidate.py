class Candidate:
    def __init__(self, election_name, name, party, profile):
        self.__candidate_id = None  # Этот атрибут будет присваиваться позже, извлечен из базы
        self.__election_name = election_name
        self.__name = name
        self.__party = party
        self.__profile = profile

    def get_id(self):
        return self.__candidate_id

    def set_id(self, candidate_id):
        self.__candidate_id = candidate_id

    def get_election_name(self):
        return self.__election_name

    def get_name(self):
        return self.__name

    def get_party(self):
        return self.__party

    def get_profile(self):
        return self.__profile

    def __str__(self):
        return f"Candidate Name: {self.__name}, Party: {self.__party}, Profile: {self.__profile}"
