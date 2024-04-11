import pymongo
import json
from bson import ObjectId

client = pymongo.MongoClient("mongodb+srv://sma_admin:nDoOqwGU4z2dBTJP@smacluster.ikhoi.mongodb.net/?retryWrites=true&w=majority&appName=smacluster")
db = client["youtubedata"]        

with open("youtube_data.json", "r") as file:
    videos = json.load(file)

for video_data in videos:
    comments = video_data.pop("comments", None)

    video_collection = db["video"]
    video_id = video_collection.insert_one(video_data).inserted_id

    if comments:
        comments_schema = []
        for comment in comments:
            comment["videoId"] = ObjectId(video_id)
            comments_schema.append(comment)

        comments_collection = db["comment"]
        comments_collection.insert_many(comments_schema)

client.close()