# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# import os
# from aiogram.types import ReplyKeyboardRemove

# from database import Database
# from keyboards import (
#     get_language_keyboard,
#     get_contact_keyboard,
#     get_games_keyboard,
#     get_admin_permission_keyboard
# )
# from utils import get_message, get_random_game_image
# from config import LANGUAGES, ADMIN_ID
# from language_manager import LanguageManager

# class UserStates(StatesGroup):
#     selecting_language = State()
#     sharing_contact = State()
#     changing_language = State()

# db = Database('users.db')
# lang_manager = LanguageManager(db)

# async def cmd_start(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     user_data = db.get_user(user_id)

#     if user_data:  # Registered user
#         await show_games_menu(message)
#     else:  # New user
#         await UserStates.selecting_language.set()
#         await message.answer(
#             get_message("start_message", "en"),
#             reply_markup=get_language_keyboard()
#         )

# async def cmd_lang(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     user_lang = lang_manager.get_user_language(user_id)

#     await UserStates.changing_language.set()
#     await message.answer(
#         get_message("select_language", user_lang),
#         reply_markup=get_language_keyboard()
#     )

# async def language_callback(callback_query: types.CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     lang_code = callback_query.data.split('_')[1]
#     current_state = await state.get_state()

#     if not lang_manager.is_valid_language(lang_code):
#         await callback_query.answer("Invalid language selection")
#         return

#     success = lang_manager.update_language(user_id, lang_code)
#     if not success:
#         await callback_query.answer("Failed to update language")
#         return

#     # Delete the message with language selection buttons
#     await callback_query.message.delete()

#     if current_state == UserStates.selecting_language.state:
#         await UserStates.sharing_contact.set()
#         await callback_query.message.answer(
#             get_message("request_contact", lang_code),
#             reply_markup=get_contact_keyboard(lang_code)
#         )
#     elif current_state == UserStates.changing_language.state:
#         await state.finish()
#         await callback_query.message.answer(
#             get_message("language_changed", lang_code)
#         )
#         await show_games_menu(callback_query.message)

#     await callback_query.answer()

# async def process_contact(message: types.Message, state: FSMContext):
#     if not message.contact:
#         return

#     user_id = message.from_user.id
#     db.save_phone(user_id, message.contact.phone_number)
#     await state.finish()

#     # Send games menu with ReplyKeyboardRemove to remove contact keyboard
#     await message.answer(
#         "✅",#get_message("select_game", db.get_user_language(user_id))",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     await message.answer(
#         get_message("select_game", db.get_user_language(user_id)),
#         reply_markup=get_games_keyboard()
#     )

# async def show_games_menu(message: types.Message):
#     user_lang = lang_manager.get_user_language(message.from_user.id)
#     await message.answer(
#         get_message("select_game", user_lang),
#         reply_markup=get_games_keyboard()
#     )

# async def process_game_selection(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_lang = lang_manager.get_user_language(user_id)
#     game_name = callback_query.data.split('_', 1)[1]

#     if not db.is_user_allowed(user_id):
#         # Get user details
#         user = callback_query.from_user
#         username = user.username if user.username else "No username"
#         full_name = f"{user.first_name} {user.last_name if user.last_name else ''}"

#         # Send detailed permission request to admin
#         admin_message = get_message("admin_permission_request", "en").format(
#             user_id=user_id,
#             username=username,
#             full_name=full_name,
#             game=game_name
#         )

#         await callback_query.bot.send_message(
#             ADMIN_ID,
#             admin_message,
#             reply_markup=get_admin_permission_keyboard(user_id)
#         )

#         # Notify user
#         await callback_query.message.answer(
#             get_message("permission_required", user_lang)
#         )
#         await callback_query.answer()
#         return

#     image_path = get_random_game_image(game_name)

#     if image_path and os.path.exists(image_path):
#         with open(image_path, 'rb') as photo:
#             await callback_query.message.answer_photo(photo, caption="Signal 📶")
#     else:
#         await callback_query.message.answer(
#             get_message("no_images", user_lang)
#         )

#     await callback_query.answer()

# async def process_admin_permission(callback_query: types.CallbackQuery):
#     action, user_id = callback_query.data.split('_')[1:]
#     user_id = int(user_id)
#     user_lang = lang_manager.get_user_language(user_id)

#     is_allowed = action == "accept"
#     db.set_user_permission(user_id, is_allowed)

#     # Notify user about the decision
#     message_key = "permission_granted" if is_allowed else "permission_denied"
#     user_message = get_message(message_key, user_lang)

#     try:
#         await callback_query.bot.send_message(
#             user_id,
#             user_message,
#             reply_markup=get_games_keyboard()
#         )
#         # Delete the admin's message with the buttons
#         await callback_query.message.delete()
#         # Confirm to admin that the action was processed
#         await callback_query.answer("User has been notified!")
#     except Exception as e:
#         # If there's an error, notify the admin
#         await callback_query.answer(f"Error: {str(e)}")



from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from aiogram.types import ReplyKeyboardRemove

from database import Database
from keyboards import (
    get_language_keyboard,
    get_contact_keyboard,
    get_games_keyboard,
    get_admin_permission_keyboard,
    get_new_image_keyboard
)
from utils import get_message, get_random_game_image
from config import LANGUAGES, ADMIN_ID, NOTIFICATION_GROUP_ID
from language_manager import LanguageManager
from ad_sender import send_advertisement

class UserStates(StatesGroup):
    selecting_language = State()
    sharing_contact = State()
    changing_language = State()
    waiting_for_ad = State()

db = Database('users.db')
lang_manager = LanguageManager(db)

async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = db.get_user(user_id)
    
    if user_data:  # Registered user
        await show_games_menu(message)
    else:  # New user
        await UserStates.selecting_language.set()
        await message.answer(
            get_message("start_message", "en"),
            reply_markup=get_language_keyboard()
        )

async def cmd_ad(message: types.Message, state: FSMContext):
    # Check if user is admin
    if message.from_user.id != ADMIN_ID:
        return
    
    await UserStates.waiting_for_ad.set()
    await message.answer("Please send the advertisement message you want to broadcast to all users:")

async def process_ad_message(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    
    await state.finish()
    await message.answer("📤 Broadcasting advertisement...")
    
    # Send the advertisement
    await send_advertisement(message.text)
    
    # Notify admin about completion
    await message.answer("✅ Advertisement has been sent to all users!")

async def cmd_lang(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = lang_manager.get_user_language(user_id)
    
    await UserStates.changing_language.set()
    await message.answer(
        get_message("select_language", user_lang),
        reply_markup=get_language_keyboard()
    )

async def language_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    lang_code = callback_query.data.split('_')[1]
    current_state = await state.get_state()
    
    if not lang_manager.is_valid_language(lang_code):
        await callback_query.answer("Invalid language selection")
        return
    
    success = lang_manager.update_language(user_id, lang_code)
    if not success:
        await callback_query.answer("Failed to update language")
        return
    
    # Delete the message with language selection buttons
    await callback_query.message.delete()
    
    if current_state == UserStates.selecting_language.state:
        await UserStates.sharing_contact.set()
        await callback_query.message.answer(
            get_message("request_contact", lang_code),
            reply_markup=get_contact_keyboard(lang_code)
        )
    elif current_state == UserStates.changing_language.state:
        await state.finish()
        await callback_query.message.answer(
            get_message("language_changed", lang_code)
        )
        await show_games_menu(callback_query.message)
    
    await callback_query.answer()

async def notify_new_user(message: types.Message, phone_number: str):
    user = message.from_user
    username = f"@{user.username}" if user.username else "No username"
    full_name = f"{user.first_name} {user.last_name if user.last_name else ''}"
    
    notification_text = (
        "🆕 New User Registered!\n\n"
        f"👤 Name: {full_name}\n"
        f"📱 Phone: {phone_number}\n"
        f"🔗 Username: {username}\n"
        f"🆔 User ID: {user.id}"
    )
    
    try:
        await message.bot.send_message(
            NOTIFICATION_GROUP_ID,
            notification_text
        )
    except Exception as e:
        print(f"Failed to send notification: {e}")

async def process_contact(message: types.Message, state: FSMContext):
    if not message.contact:
        return
    
    user_id = message.from_user.id
    user_lang = db.get_user_language(user_id)
    phone_number = message.contact.phone_number
    db.save_phone(user_id, phone_number)
    await state.finish()
    
    # Send notification to the group
    await notify_new_user(message, phone_number)

    await message.answer(
#         "✅",#get_message("select_game", db.get_user_language(user_id))",
#         reply_markup=ReplyKeyboardRemove()
#     )
    
    # First remove the contact keyboard and show welcome message
    await message.answer(
        get_message("contact_received", user_lang),
        reply_markup=get_games_keyboard()
    )

async def show_games_menu(message: types.Message):
    user_lang = lang_manager.get_user_language(message.from_user.id)
    await message.answer(
        get_message("select_game", user_lang),
        reply_markup=get_games_keyboard()
    )

async def send_game_image(message: types.Message, game_name: str, user_lang: str):
    image_path = get_random_game_image(game_name)
    
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as photo:
            await message.answer_photo(
                photo,
                reply_markup=get_new_image_keyboard(game_name)
            )
    else:
        await message.answer(
            get_message("no_images", user_lang)
        )

async def process_game_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_lang = lang_manager.get_user_language(user_id)
    game_name = callback_query.data.split('_', 1)[1]
    
    if not db.is_user_allowed(user_id):
        # Get user details
        user = callback_query.from_user
        username = user.username if user.username else "No username"
        full_name = f"{user.first_name} {user.last_name if user.last_name else ''}"
        
        # Send detailed permission request to admin
        admin_message = get_message("admin_permission_request", "en").format(
            user_id=user_id,
            username=username,
            full_name=full_name,
            game=game_name
        )
        
        await callback_query.bot.send_message(
            ADMIN_ID,
            admin_message,
            reply_markup=get_admin_permission_keyboard(user_id)
        )
        
        # Notify user
        await callback_query.message.answer(
            get_message("permission_required", user_lang)
        )
        await callback_query.answer()
        return
    
    await send_game_image(callback_query.message, game_name, user_lang)
    await callback_query.answer()

async def process_new_image(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_lang = lang_manager.get_user_language(user_id)
    game_name = callback_query.data.split('_', 1)[1]
    
    # Delete the previous image
    await callback_query.message.delete()
    
    # Send a new image
    await send_game_image(callback_query.message, game_name, user_lang)
    await callback_query.answer()

async def process_admin_permission(callback_query: types.CallbackQuery):
    action, user_id = callback_query.data.split('_')[1:]
    user_id = int(user_id)
    user_lang = lang_manager.get_user_language(user_id)
    
    is_allowed = action == "accept"
    db.set_user_permission(user_id, is_allowed)
    
    # Notify user about the decision
    message_key = "permission_granted" if is_allowed else "permission_denied"
    user_message = get_message(message_key, user_lang)
    
    try:
        # First send the permission message
        await callback_query.bot.send_message(
            user_id,
            user_message
        )
        
        # If permission was granted, show the games menu
        if is_allowed:
            await callback_query.bot.send_message(
                user_id,
                get_message("select_game", user_lang),
                reply_markup=get_games_keyboard()
            )
        
        # Delete the admin's message with the buttons
        await callback_query.message.delete()
        # Confirm to admin that the action was processed
        await callback_query.answer("User has been notified!")
    except Exception as e:
        # If there's an error, notify the admin
        await callback_query.answer(f"Error: {str(e)}")
