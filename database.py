from pymongo import MongoClient

client = MongoClient('mongodb+srv://shadow:xshadow@filesharebot.s8qpy.mongodb.net/?retryWrites=true&w=majority&appName=fileShareBot')
db = client['users']
 
# SQLite3 database helper
class DBHelper:
    def __init__(self, dbname="users"):
        self.dbname = dbname
        self.collection = db[dbname]

    # Check if a user exists in the database
    def user_exists(self, user_id):
        return self.collection.find_one({"user_id": user_id}) is not None
        
        

    # Add a new user to the database
    def add_user(self, user_id, username, first_name):
        if not self.user_exists(user_id):
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "counter": 0,
                "authenticated": False,
                "auth_key": None,
                "deauthentication_time": None
            }
            
            self.collection.insert_one(user_data)

    # Get the counter value for a user
    def get_counter(self, user_id):
        counter = self.collection.find_one({"user_id": user_id}, {"counter": 1})
        
        if counter and "counter" in counter:
            return counter["counter"]
        else:
            return 0
    
    # Update the counter value for a user
    def update_counter(self, user_id, counter):
        self.collection.update_one({"user_id": user_id}, {"$set": {"counter": counter}})

    # Check if a user is authenticated
    def is_authenticated(self, user_id):
        authenticated = self.collection.find_one({"user_id": user_id}, {"authenticated": 1})
        if authenticated:
            return authenticated["authenticated"]
        else:
            return False
    
    # Add an authentication key to the database for a user
    def addAuthKeyToDatabase(self, user_id, auth_key):
        self.collection.update_one({"user_id": user_id}, {"$set": {"auth_key": auth_key}})

    # Get the authentication key for a user
    def getAuthKey(self, user_id):
        auth_key = self.collection.find_one({"user_id": user_id}, {"auth_key": 1})
         
        if auth_key and "auth_key" in auth_key:
            
            return auth_key["auth_key"]
        else:
            return None
        
    # Update the authentication status for a user
    def update_authentication(self, user_id, authenticated):
        self.collection.update_one({"user_id": user_id}, {"$set": {"authenticated": authenticated}})

    # Update the deauthentication time for a user
    def update_deauthentication_time(self, deauth_time, user_id):
        self.collection.update_one({"user_id": user_id}, {"$set": {"deauthentication_time": deauth_time}})

    # Get the deauthentication time for a user
    def get_deauthentication_time(self, user_id):
        deauth_time = self.collection.find_one({"user_id": user_id}, {"deauthentication_time": 1})
        
        if deauth_time:
            return deauth_time["deauthentication_time"]
        else:
            return None

    # Set the authentication key to null for a user
    def setAuthKeyToNull(self, user_id):
        self.collection.update_one({"user_id": user_id}, {"$set": {"auth_key": None}})
    
    # Get all users from the database
    def get_all_users(self):
        return list(self.collection.find())
    
    # Move a user to the blocked_users table
    def move_user_to_blocked_table(self, user_id):
        # Remove user from the main collection
        self.collection.delete_one({"user_id": user_id})
        
        # Add user to the blocked_users collection
        blocked_user_data = {"user_id": user_id}
        db["blocked_users"].insert_one(blocked_user_data)
