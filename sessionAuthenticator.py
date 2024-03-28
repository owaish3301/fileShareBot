from database import DBHelper


async def sessionAuthenticator(user_id, counter):
    db = DBHelper()
    if counter < 4:
        counter += 1
        db.update_counter(user_id, counter)
        return 'authenticated'
        
    elif counter == 4:
        # Check if the user is authenticated
        authenticated = db.is_authenticated(user_id)
        
        if authenticated:
            return 'authenticated'
        else:
            return 'unauthenticated'

