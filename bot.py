# import logging
# from aiogram import Bot, Dispatcher, executor
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from config import API_TOKEN
# from handlers import (
#     cmd_start,
#     cmd_lang,
#     language_callback,
#     process_contact,
#     process_game_selection,
#     process_admin_permission,
#     UserStates
# )

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Initialize bot and dispatcher
# bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)

# # Register handlers
# dp.register_message_handler(cmd_start, commands=['start'])
# dp.register_message_handler(cmd_lang, commands=['lang'])
# dp.register_callback_query_handler(
#     language_callback,
#     lambda c: c.data and c.data.startswith('lang_'),
#     state=[UserStates.selecting_language, UserStates.changing_language]
# )
# dp.register_message_handler(
#     process_contact,
#     content_types=['contact'],
#     state=UserStates.sharing_contact
# )
# dp.register_callback_query_handler(
#     process_game_selection,
#     lambda c: c.data and c.data.startswith('game_')
# )
# dp.register_callback_query_handler(
#     process_admin_permission,
#     lambda c: c.data and c.data.startswith('permit_')
# )

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

# #


import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN
from handlers import (
    cmd_start,
    cmd_lang,
    language_callback,
    process_contact,
    process_game_selection,
    process_admin_permission,
    process_new_image,
    UserStates
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Register handlers
dp.register_message_handler(cmd_start, commands=['start'])
dp.register_message_handler(cmd_lang, commands=['lang'])
dp.register_callback_query_handler(
    language_callback,
    lambda c: c.data and c.data.startswith('lang_'),
    state=[UserStates.selecting_language, UserStates.changing_language]
)
dp.register_message_handler(
    process_contact,
    content_types=['contact'],
    state=UserStates.sharing_contact
)
dp.register_callback_query_handler(
    process_game_selection,
    lambda c: c.data and c.data.startswith('game_')
)
dp.register_callback_query_handler(
    process_admin_permission,
    lambda c: c.data and c.data.startswith('permit_')
)
dp.register_callback_query_handler(
    process_new_image,
    lambda c: c.data and c.data.startswith('new_')
)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)