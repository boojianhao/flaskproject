class Users:
    user_id = 0
    def __init__(self, email, password, name, security_question_1, security_question_2, active=True):
        Users.user_id += 1
        self.__email = email
        self.__password = password
        self.__name = name
        self.__security_question_1 = security_question_1
        self.__security_question_2 = security_question_2
        self.__active = active

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_user_id(self):
        return self.__user_id

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

    def set_name(self, name):
        self.__name = name

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
