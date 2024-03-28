from database import DBHelper
import re
from config import TOKEN
from aiogram import Bot

bot = Bot(TOKEN)

async def broadcast_message(msg):
    # Get all the users from the database
    db = DBHelper()
    users = db.get_all_users()
    for user in users:
        try:
            if msg.text:
                # Send the message to all the users
                await bot.send_message(chat_id=user['user_id'], text=msg.text)
            else:
                await bot.send_photo(chat_id=user['user_id'], photo=msg.photo[-1].file_id, caption=msg.caption)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            error_message = str(e)
            if re.search(r'bot was blocked by the user', error_message):
                db.move_user_to_blocked_table(user['user_id'])
                
    await msg.answer("message broadcasted successfully")