class Users:
    def __init__(self, email, password, name):
        self.__email = email
        self.__password = password
        self.__name = name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name
