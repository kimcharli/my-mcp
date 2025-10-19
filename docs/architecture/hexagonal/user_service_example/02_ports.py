# 02_ports.py

from abc import ABC, abstractmethod
from typing import Optional

from domain import User

# Primary Port
class UserService(ABC):
    @abstractmethod
    def register_user(self, email: str, password: str) -> User:
        pass

# Secondary Port
class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass
