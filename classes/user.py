class User:
    def __init__(self, username, password, email, phone_number):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__phone_number = phone_number

    def get_username(self):
        return self.__username
    def set_username(self, username):
        self.__username = username

    def get_email(self):
        return self.__email
    def set_email(self, email):
        self.__email = email

    def get_password(self):
        return self.__password
    def set_password(self, password):
        self.__password = password

    def get_phone_number(self):
        return self.__phone_number
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def __str__(self):
        return f"Username: {self.__username}, Email: {self.__email}, Password: {self.__password}, Phone Number: {self.__phone_number}"