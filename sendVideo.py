from config import TOKEN
from aiogram import Bot

bot = Bot(token=TOKEN)

#function to send video , will be called form start_function
async def sendVideo(user_id: str, videoId: str, caption: str) -> None:
    if videoId is not None:
        try:
            await bot.send_video(chat_id=user_id, video=videoId, caption=caption)
        except Exception as e:
            await bot.send_message(chat_id=user_id, text="Video not found.")    
    else:
        await bot.send_message(chat_id=user_id, text="Video not found.")