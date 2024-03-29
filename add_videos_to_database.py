from datetime import datetime
from pymongo import MongoClient
from config import mongodbUrl


# Function to add video to json file
def add_video_to_database(unique_id, video_id, caption):
    try:
        # Create a MongoClient to the running mongod instance
        client = MongoClient(mongodbUrl)

        # Get the database
        db = client['videos']  # replace 'your_database' with your database name

        # Get the collection
        collection = db['videos']  # replace 'your_collection' with your collection name

        # Add new video data
        video_data = {
            "_id": unique_id,
            "videoId": video_id,
            "caption": caption,
            "uploadDate": datetime.now().strftime('%Y-%m-%d')
        }

        # Insert the video data into the collection
        collection.insert_one(video_data)
    except Exception as e:
        print(f"An error occurred while adding video to database: {e}")
