# 01_domain.py

import re

class InvalidEmailError(Exception):
    pass

class User:
    def __init__(self, email: str, password: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise InvalidEmailError("Invalid email format")
        self.email = email
        self.password = password

    def verify_password(self, password: str) -> bool:
        return self.password == password
