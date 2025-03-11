import os
from pathlib import Path

# Bot token
API_TOKEN = '7224582081:AAGUnuel3rWaUAiYu_XUOdsoObRPB0WXWRw'  # Replace with your actual bot token

# Database
DB_NAME = 'users.db'

# Game folders
GAMES = [
    "Gems & Mines",
    "Game Of Thrones",
    "Dragon's Gold",
    "Eastern nights",
    "Swamp Land",
    "Apple Of Fortune",
]

# Create game directories
for game in GAMES:
    os.makedirs(f"games/{game}", exist_ok=True)

# Supported languages
LANGUAGES = {
    'en': '🇬🇧 English',
    'ru': '🇷🇺 Russian',
    'uz': '🇺🇿 Uzbek'
}

NOTIFICATION_GROUP_ID = -1002333388565

ADMIN_ID = 7645882735#5235865310