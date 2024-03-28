import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv(".env")

# Get variables from environment
TOKEN = os.getenv("TOKEN")
print(TOKEN)
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS").split(",")]
bot_username = os.getenv("bot_username")
force_sub_channel_id = int(os.getenv("force_sub_channel_id"))
force_sub_channel_link = os.getenv("force_sub_channel_link")
tutorialVideoId = os.getenv("tutorialVideoId")