class Users:
    def __init__(self, email, password, name, security_question_1, security_question_2, active=True):
        self.__email = email
        self.__password = password
        self.__name = name
        self.__security_question_1 = security_question_1
        self.__security_question_2 = security_question_2
        self.__active = active

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_security_question_1(self):
        return self.__security_question_1

    def get_security_question_2(self):
        return self.__security_question_2

    def is_active(self):
        return self.__active

    def is_admin(self):
        return False

    def is_driver(self):
        return False

    def deactivate(self):
        self.__active = False