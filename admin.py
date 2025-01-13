# admin.py
from Users import Users

class Admin(Users):
    def __init__(self, email, password, name, security_question_1, security_question_2, active=True):
        super().__init__(email, password, name, security_question_1, security_question_2, active)

    def is_admin(self):
        return True

    def create_user(self, user_dict, new_user):
        user_dict[new_user.get_email()] = new_user

    def delete_user(self, user_dict, email):
        if email in user_dict:
            del user_dict[email]

    def create_driver(self, user_dict, email, password, name, security_question_1, security_question_2):
        new_driver = Users(email, password, name, security_question_1, security_question_2, active=True)
        self.create_user(user_dict, new_driver)