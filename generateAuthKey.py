import secrets
from database import DBHelper

def generateAuthKey(user_id):
    try:
        # Generate a random key
        auth_key = secrets.token_urlsafe(16)
        
        db = DBHelper()
        # Add the key to the database
        db.addAuthKeyToDatabase(user_id, auth_key)

        return auth_key

    except Exception as e:
        # Handle any exceptions that occur
        print(f"An error occurred: {e}")
        return None


def setAuthKey_to_Null(user_id):
    try:
        db = DBHelper()
        # Set the authentication key to null
        db.setAuthKeyToNull(user_id)
    except Exception as e:
        print(f"An error occurred: {e}")