# admin.py
from customer import Users

class Admin(Users):
    def __init__(self, email, password, name, security_question_1, security_question_2, active=True):
        super().__init__(email, password, name, security_question_1, security_question_2, active)

    def is_admin(self):
        return True