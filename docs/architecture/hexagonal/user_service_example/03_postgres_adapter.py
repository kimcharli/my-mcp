# 03_postgres_adapter.py

from typing import Optional

import psycopg2

from domain import User
from ports import UserRepository

class PostgresUserRepository(UserRepository):
    def __init__(self, db_url: str):
        self.db_url = db_url

    def find_by_email(self, email: str) -> Optional[User]:
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return User(email=row[0], password=row[1])
        return None

    def save(self, user: User) -> None:
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (user.email, user.password))
        conn.commit()
        cursor.close()
        conn.close()
