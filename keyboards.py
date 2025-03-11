from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import LANGUAGES, GAMES

def get_language_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    # First row: Uzbek and Russian
    keyboard.row(
        InlineKeyboardButton(
            text="🇺🇿 Uzbek",
            callback_data="lang_uz"
        ),
        InlineKeyboardButton(
            text="🇷🇺 Russian",
            callback_data="lang_ru"
        )
    )
    # Second row: English
    keyboard.row(
        InlineKeyboardButton(
            text="🇬🇧 English",
            callback_data="lang_en"
        )
    )
    return keyboard

def get_contact_keyboard(lang: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text="📱 Share Contact", request_contact=True)
    keyboard.add(button)
    return keyboard

def get_games_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    games = GAMES[:-1]  # All games except the last one
    last_game = GAMES[-1]  # Last game

    # Add games in pairs
    for i in range(0, len(games), 2):
        row = []
        for game in games[i:i+2]:
            row.append(InlineKeyboardButton(
                text=game,
                callback_data=f"game_{game}"
            ))
        keyboard.row(*row)

    # Add last game in separate row
    keyboard.row(InlineKeyboardButton(
        text=last_game,
        callback_data=f"game_{last_game}"
    ))

    return keyboard

def get_admin_permission_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton(
            text="✅ Accept",
            callback_data=f"permit_accept_{user_id}"
        ),
        InlineKeyboardButton(
            text="❌ Reject",
            callback_data=f"permit_reject_{user_id}"
        )
    )
    return keyboard

def get_new_image_keyboard(game_name: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        text="🔄 New",
        callback_data=f"new_{game_name}"
    ))
    return keyboard