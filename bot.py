#necessary imports
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import Router
from aiogram import types
from aiogram import F

 
#custom imports
from config import TOKEN, ADMIN_IDS, bot_username, force_sub_channel_id, tutorialVideoId
from getVideo import getVideo
from argumentGenerator import generate_unique_id
from sendVideo import sendVideo
from add_videos_to_database import add_video_to_database
from database import DBHelper
from sessionAuthenticator import sessionAuthenticator
from generateAuthKey import generateAuthKey, setAuthKey_to_Null
from inlineKeyboards import unauthenicated_users_inline_keyboard, force_sub_inline_keyboard
from shortendLink import short_url
from deauthenticate_users import update_deauth_time, deauthenticate_user
from broadcast import broadcast_message




#important variables
canSaveVideo = False
canBroadcast = False

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

bot = Bot(TOKEN)

dp = Dispatcher()

router = Router()

        
    
#/start handler
@router.message(Command("start"))
async def start_function(msg: types.message) -> None:

    # Extract the user's name and id
    user_id = msg.chat.id
    username = msg.chat.username
    name = msg.chat.first_name

    # Create an instance of the DBHelper class
    db = DBHelper()
    db.add_user(user_id, username, name) # Add the user to the database if they don't exist

    
    # Extract unique string from the command
    commandArgument = msg.text.split(" ")[1] if len(msg.text.split(" ")) > 1 else None   
    

    if commandArgument:
        try:
            member = await bot.get_chat_member(chat_id=force_sub_channel_id, user_id=user_id)
        except:
            member = None

        try:
            # Check if the user is a member of the channel
            if member.status in ["creator", "administrator", "member"]:

                if commandArgument == db.getAuthKey(user_id): # Check if the command argument is the authentication key
                    db.update_authentication(user_id, True) # Update the authentication status of the user
                    await msg.answer("✅Your token is successfully verified and is valid for next 24 hours. You can now access any video for free.✅ \n \nClick on the link again to get the video.")
                    
                    update_deauth_time(user_id) # Update the deauthentication time for the user
                    setAuthKey_to_Null(user_id) # Set the authentication key to None
                  
                    return
                
                # Fetch the counter from the database for the user_id
                counter = db.get_counter(user_id)

                isAuthenticated = await sessionAuthenticator(user_id, counter) # Authenticate the user

                if isAuthenticated == 'authenticated':

                    is_deauthenticated = await deauthenticate_user(user_id, msg) # Deauthenticate the user if the deauthentication time has passed
                    
                    if is_deauthenticated == 1:
                        # Get the videoId and caption from the json file if the user sends /start command with an argument
                        videoId, caption = await getVideo(commandArgument)

                        # Send the video by calling sendVideo function
                        await sendVideo(user_id, videoId, caption)
                elif isAuthenticated == 'unauthenticated':
                    key = generateAuthKey(user_id) # Generate an authentication key for the user
                    
                    if key is not None:
                        url = f"https://t.me/{bot_username}?start={key}"
                        
                        short_link = short_url(url)
                        if short_link is not None:   
                            inline_keyboard = unauthenicated_users_inline_keyboard(short_link) # Create an inline keyboard for the unauthenticated users
                        else:
                            msg.answer("An error occurred please try again later.")

                        await msg.answer(f'Hello {name},\nYour Ads token is expired, please click on the link below👇 . \n\nIf you pass one ad you can watch free videos for next 24 hours ', reply_markup=inline_keyboard)
                    else:
                        await msg.answer("An error occurred please try again later.")
            else:
                # Call the notMember function if the user is not a member of the channel
                await notMember(msg,name)
                
        except Exception as e:
            print(f"An error occurred in the start function: {str(e)}")
            
    else:
        # Send the welcome message when the user sends /start command without any argument
        await msg.answer(text=f"Hello {name}\nI can store private files and other users can access them by a special link")
    
async def notMember(msg,name) -> None:
    inline_keyboard = force_sub_inline_keyboard() # Create an inline keyboard for the unauthenticated users
    # Send the welcome message when the user sends /start command with an argument and is not a member of the channel
    await msg.answer(text=f"Hello {name},\nIt seems like you haven't joined our channel yet. Please join our channel and click on link again to use this bot and watch the video.", reply_markup=inline_keyboard)

# /callback handler
@router.callback_query()
async def callback_handler(query: types.CallbackQuery) -> None:
    # Extract the callback data
    callback_data = query.data
    
    if callback_data == 'tutorial':
        # Send the tutorial video
        await sendVideo(query.from_user.id, tutorialVideoId, caption="Watch this video to learn how to open the link")

# /genLink handler
@router.message(Command("genLink"),F.from_user.id.in_(ADMIN_IDS))
async def genLink(msg: types.message) -> None:
    global canSaveVideo
    
    await msg.answer("send a video to generate a link")
    canSaveVideo = True

# /broadcast handler
@router.message(Command("broadcast"),F.from_user.id.in_(ADMIN_IDS))
async def broadcast(msg: types.message) -> None:
    global canBroadcast

    await msg.answer("send a message to broadcast")
    canBroadcast = True

# /subscribe handler
@router.message(Command("subscribers"), F.from_user.id.in_(ADMIN_IDS))
async def subscribers(msg: types.message) -> None:
    try:
        db = DBHelper()
        # Get the number of subscribers
        subscribers = db.get_all_users()
        
        num_subscribers = len(subscribers)
        await msg.answer(f"Total subscribers: {num_subscribers}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



# Save the video
@router.message(F.from_user.id.in_(ADMIN_IDS), F.video)
async def saveVideo(msg: types.video) -> None:
    global canSaveVideo
    try:
        if canSaveVideo == True:
            
            video_id = msg.video.file_id
            caption = msg.caption if msg.caption else ""
            #canSaveVideo = False

            # Generate a unique id for the video
            unique_id = generate_unique_id() 

            # Add the video to the json file
            add_video_to_database(unique_id, video_id, caption)
            await msg.answer("video saved successfully")
            
            #await bot.send_video(chat_id=msg.chat.id, video= video_id, caption=f"https://t.me/{bot_username}?start={unique_id}")
            # Send the link to the user
            await msg.answer( f"Link: https://t.me/{bot_username}?start={unique_id}")
        else:
            await msg.answer("send /genLink to generate a link")   
    except Exception as e:
        await msg.answer(f"An error occurred: {str(e)}")


@router.message(F.from_user.id.in_(ADMIN_IDS), F.text | F.photo)
async def broadcastMessage(msg: types.message) -> None:
    global canBroadcast
    try:
        if canBroadcast == True:
            canBroadcast = False
            await broadcast_message(msg)
            
        else:
            await msg.answer("send /broadcast to broadcast a message")
    except Exception as e:
        await msg.answer(f"An error occurred: {str(e)}")
        


   

#main function
async def main() -> None:
    
    dp.include_router(router) 
    await dp.start_polling(bot)



print('bot started...')
if __name__ == '__main__':
    asyncio.run(main())
