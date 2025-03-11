import json
import random
import os
from typing import Dict, Any

def load_languages() -> Dict[str, Dict[str, str]]:
    with open('lang.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_message(message_key: str, lang: str) -> str:
    languages = load_languages()
    return languages.get(message_key, {}).get(lang, "Message not found")

def get_random_game_image(game_name: str) -> str:
    game_dir = f"games/{game_name}"
    if not os.path.exists(game_dir):
        return None

    images = [f for f in os.listdir(game_dir)
              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    return os.path.join(game_dir, random.choice(images)) if images else None

