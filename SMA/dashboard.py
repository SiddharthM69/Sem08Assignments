import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from googleapiclient.discovery import build
from textblob import TextBlob
import re

# Set up YouTube API access
api_key = "AIzaSyBP29jlFl-NOJiGyK8O5FsOnIt6IGTFFwU"
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to fetch video data
def get_channel_videos(channel_id):
    res = youtube.channels().list(id=channel_id,
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return videos

# Function to fetch comments for a video
def get_video_comments(video_id):
    comments = []
    next_page_token = None

    while True:
        res = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            textFormat='plainText',
            pageToken=next_page_token
        ).execute()

        for item in res['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            cleaned_comment = clean_text(comment)
            comments.append(cleaned_comment)

        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return comments

# Function to clean text
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text

# Fetching videos from a channel
channel_id = "UCBwmMxybNva6P_5VmxjzwqA"
videos = get_channel_videos(channel_id)

# Extracting data
video_data = []
i=0
for video in videos:
    if i==20:
        break
    video_id = video['snippet']['resourceId']['videoId']
    title = video['snippet']['title']
    # Fetch video statistics separately
    video_stats = youtube.videos().list(id=video_id, part='statistics').execute()
    views = video_stats['items'][0]['statistics'].get('viewCount', 0)
    comments = get_video_comments(video_id)
    video_data.append({'Title': title, 'Views': views, 'Comments': comments})
    i+=1

# Convert data to DataFrame
df = pd.DataFrame(video_data)

# Sentiment analysis
df['Sentiment'] = df['Comments'].apply(lambda x: TextBlob(' '.join(x)).sentiment.polarity)

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("YouTube Data Visualization Dashboard For Apna College"),
    dcc.Graph(id='sentiment-graph for 20 latest videos'),
    dcc.Graph(id='views-comments-graph for 20 latest videos'),
    dcc.Graph(id='total-views-bar for 20 latest videos'),
    dcc.Graph(id='comments-length-hist for 20 latest videos')
])

# Define callbacks
@app.callback(
    [Output('sentiment-graph for 20 latest videos', 'figure'),
     Output('views-comments-graph for 20 latest videos', 'figure'),
     Output('total-views-bar for 20 latest videos', 'figure'),
     Output('comments-length-hist for 20 latest videos', 'figure')],
    [Input('sentiment-graph for 20 latest videos', 'id')]
)
def update_graphs(sentiment_id):
    # Sentiment analysis scatter plot
    sentiment_fig = px.scatter(df, x='Views', y='Sentiment', hover_data=['Title'],
                               title='Sentiment Analysis of Video Comments')
    
    # Views vs Comments scatter plot
    views_comments_fig = px.scatter(df, x='Views', y=df['Comments'].apply(len),
                                    hover_data=['Title'], title='Views vs Comments on Videos')
    
    # Total views bar chart
    total_views_fig = px.bar(df, x='Title', y='Views', title='Total Views for Each Video')
    
    # Comments length histogram
    comments_length_fig = px.histogram(df, x=df['Comments'].apply(lambda x: len(' '.join(x))),
                                       title='Distribution of Comments Length')
    
    return sentiment_fig, views_comments_fig, total_views_fig, comments_length_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
