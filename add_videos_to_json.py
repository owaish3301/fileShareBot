from datetime import datetime
import json


# Function to add video to json file
def add_video_to_json(unique_id, video_id, caption):
    try:
        with open('videos.json', 'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

            # Add new video data
            file_data[unique_id] = {
                "videoId": video_id,
                "caption": caption,
                "uploadDate": datetime.now().strftime('%Y-%m-%d')
            }
            # Sets file's current position at offset.
            file.seek(0)

            # convert back to json.
            json.dump(file_data, file, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")
