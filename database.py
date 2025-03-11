import sqlite3
from typing import Optional, Tuple
import os

class Database:
    def __init__(self, db_name: str):
        # Delete the existing database file if it exists
        if os.path.exists(db_name):
            os.remove(db_name)

        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users
                        (user_id INTEGER PRIMARY KEY,
                         language TEXT,
                         phone TEXT,
                         is_allowed BOOLEAN DEFAULT FALSE)''')
            conn.commit()

    def get_user(self, user_id: int) -> Optional[Tuple[str, str, bool]]:
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('SELECT language, phone, is_allowed FROM users WHERE user_id = ?', (user_id,))
            result = c.fetchone()
            return result if result else None

    def save_language(self, user_id: int, language: str):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO users (user_id, language, is_allowed)
                        VALUES (?, ?, FALSE)
                        ON CONFLICT(user_id) DO UPDATE SET language = ?''',
                     (user_id, language, language))
            conn.commit()

    def save_phone(self, user_id: int, phone: str):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''UPDATE users SET phone = ? WHERE user_id = ?''',
                     (phone, user_id))
            conn.commit()

    def get_user_language(self, user_id: int) -> str:
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
            result = c.fetchone()
            return result[0] if result else 'en'

    def set_user_permission(self, user_id: int, is_allowed: bool):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''UPDATE users SET is_allowed = ? WHERE user_id = ?''',
                     (is_allowed, user_id))
            conn.commit()

    def is_user_allowed(self, user_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('SELECT is_allowed FROM users WHERE user_id = ?', (user_id,))
            result = c.fetchone()
            return bool(result[0]) if result else False