from typing import Optional
from database import Database

class LanguageManager:
    def __init__(self, db: Database):
        self.db = db

    def get_user_language(self, user_id: int) -> str:
        """Get user's current language"""
        return self.db.get_user_language(user_id)

    def update_language(self, user_id: int, new_language: str) -> bool:
        """Update user's language preference"""
        try:
            self.db.save_language(user_id, new_language)
            return True
        except Exception:
            return False

    def is_valid_language(self, lang_code: str) -> bool:
        """Check if the language code is valid"""
        return lang_code in ['en', 'ru', 'uz']