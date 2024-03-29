from pymongo import MongoClient
from config import mongodbUrl

# Function to get video from MongoDB
async def getVideo(commandArgument: str) -> str:
    try:
        # Create a MongoClient to the running mongod instance
        client = MongoClient(mongodbUrl)  # replace 'mongodbUrl' with your MongoDB URL

        # Get the database
        db = client['videos']  # replace 'your_database' with your database name

        # Get the collection
        collection = db['videos']  # replace 'your_collection' with your collection name

        # Find the video data
        video_data = collection.find_one({"_id": commandArgument})

        if video_data is not None:
            return video_data['videoId'], video_data['caption']
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")