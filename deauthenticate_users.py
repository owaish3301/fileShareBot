import datetime
from database import DBHelper

def update_deauth_time(user_id):
    try:
        db = DBHelper()
        # Get the current time and date
        current_time = datetime.datetime.now()

        # Add 24 hours to the current time
        deauth_time = current_time + datetime.timedelta(hours=24)

        # Update the deauthentication_time in the database
        db.update_deauthentication_time(deauth_time, user_id)
    except Exception as e:
        print(f"An error occurred while updating deauthentication time: {e}")


async def deauthenticate_user(user_id, msg):
    try:
        db = DBHelper()
        deauth_time_str = db.get_deauthentication_time(user_id)  # Get the deauthentication time for the user
        
        if deauth_time_str is None:
            return 1
        deauth_time = datetime.datetime.strptime(str(deauth_time_str), "%Y-%m-%d %H:%M:%S.%f")

        current_time = datetime.datetime.now()
        if current_time > deauth_time:
            db.update_authentication(user_id, False)  # Update the authentication status of the user
            await msg.answer("❌Your token has expired. Please click on the link again to get a new token.❌")
            return 0
        else:
            return 1
    except Exception as e:
        print(f"An error occurred while deauthenticating user: {e}")
