import os
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from collections import Counter
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd

api_key = "AIzaSyBP29jlFl-NOJiGyK8O5FsOnIt6IGTFFwU"
video_id = "KGQSTDm5ois"
max_results = 100
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()


def get_comments(video_id, max_results):
    comments = []
    nextPageToken = None
    while True:
        response = (
            youtube.commentThreads()
            .list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                pageToken=nextPageToken,
            )
            .execute()
        )
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        if "nextPageToken" in response:
            nextPageToken = response["nextPageToken"]
        else:
            break
    return comments


comments = get_comments(video_id, max_results)
print("Total Number of Comments:", len(comments))

print("\nFirst 20 Comments:")
for i, comment in enumerate(comments[:20], start=1):
    print(f"{i}. {comment}")

# Write comments to CSV file
df = pd.DataFrame({"Comments": comments})
df.to_csv("comments.csv", index=False)
print("Comments written to comments.csv file.")

