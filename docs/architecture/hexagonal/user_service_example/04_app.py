# 04_app.py

from domain import User
from ports import UserService, UserRepository

class UserServiceImpl(UserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, email: str, password: str) -> User:
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("User already exists")
        user = User(email=email, password=password)
        self.user_repository.save(user)
        return user
