import json

#function to get video from json file   
async def getVideo(commandArgument: str) -> str:
    with open('videos.json', 'r') as file:
        data = json.load(file)
        if commandArgument in data:
            return data[commandArgument]['videoId'], data[commandArgument]['caption']
        else:
            return None, None
        