class Election:
    def __init__(self,  name, start_date, end_date):
        self.__name = name
        self.__start_date = start_date
        self.__end_date = end_date

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name

    def get_start_date(self):
        return self.__start_date
    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_end_date(self):
        return self.__end_date
    def set_end_date(self, end_date):
        self.__end_date = end_date

    def __str__(self):
        return f"Election Name: {self.__name}, Start Date: {self.__start_date}, End Date: {self.__end_date}"

