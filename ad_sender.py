from aiogram import Bot
from database import Database
from config import API_TOKEN
import asyncio
from typing import Union, List

class AdSender:
    def __init__(self):
        self.bot = Bot(token=API_TOKEN)
        self.db = Database('users.db')

    async def send_ad_to_user(self, user_id: int, message: str, media: Union[str, None] = None) -> bool:
        """
        Send advertisement to a single user
        Returns True if message was sent successfully, False otherwise
        """
        try:
            if media:
                with open(media, 'rb') as photo:
                    await self.bot.send_message(
                        chat_id=user_id,
                        text=message
                    )
            else:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message
                )
            await asyncio.sleep(0.1)  # Rate limiting
            return True
        except Exception as e:
            print(f"Failed to send ad to user {user_id}: {str(e)}")
            return False

    async def broadcast_ad(self, message: str, media: Union[str, None] = None) -> dict:
        """
        Broadcast advertisement to all users
        Returns dictionary with success and failure counts
        """
        users = self.db.get_all_users()
        results = {
            'total': len(users),
            'success': 0,
            'failed': 0
        }

        for user_id in users:
            success = await self.send_ad_to_user(user_id, message, media)
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1

        return results

async def send_advertisement(message: str, media_path: Union[str, None] = None) -> dict:
    """
    Helper function to send advertisement
    Returns the results dictionary
    """
    sender = AdSender()
    return await sender.broadcast_ad(message, media_path)
