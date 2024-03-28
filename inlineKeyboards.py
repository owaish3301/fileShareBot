from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import force_sub_channel_link

def unauthenicated_users_inline_keyboard(short_link):
    # Create an inline keyboard
    button1 = InlineKeyboardButton(text="👉Click here👈", url=short_link)
    button2 = InlineKeyboardButton(text="Click to Watch Tutorial", callback_data='tutorial')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])
    return keyboard

def force_sub_inline_keyboard():
    # Create an inline keyboard
    button = InlineKeyboardButton(text="Join Channel😍",url=force_sub_channel_link)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return keyboard
