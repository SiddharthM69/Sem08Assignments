import dash
from dash import dcc, html, Input, Output
from googleapiclient.discovery import build
import plotly.express as px

# YouTube Data API credentials
API_KEY = "AIzaSyBP29jlFl-NOJiGyK8O5FsOnIt6IGTFFwU"

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to fetch real-time YouTube data
def get_youtube_data(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()
    subscriber_count = response['items'][0]['statistics']['subscriberCount']
    view_count = response['items'][0]['statistics']['viewCount']
    video_count = response['items'][0]['statistics']['videoCount']
    return subscriber_count, view_count, video_count

# Function to fetch real-time comments from YouTube video
def get_video_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()
    comments = []
    for item in response['items']:
        comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
    return comments

# Dash app layout
app.layout = html.Div([
    html.H1("YouTube Analytics Dashboard"),
    html.Label("Enter YouTube Channel ID:"),
    dcc.Input(id="channel-id", type="text", placeholder="Enter channel ID..."),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id="output-container-button",
             children='Enter a value and press submit'),
    html.Div(id="dashboard-content")
])

# Callback to update the dashboard content
@app.callback(
    Output('dashboard-content', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('channel-id', 'value')]
)
def update_dashboard(n_clicks, channel_id):
    if n_clicks > 0:
        subscriber_count, view_count, video_count = get_youtube_data(channel_id)
        return html.Div([
            html.H2("Channel Statistics"),
            html.P(f"Subscriber Count: {subscriber_count}"),
            html.P(f"Total Views: {view_count}"),
            html.P(f"Total Videos: {video_count}"),
            html.H2("Recent Video Comments"),
            dcc.Loading(
                id="loading-1",
                children=[html.Div(id="comments-container")],
                type="default"
            )
        ])

# Callback to fetch and display recent comments
@app.callback(
    Output("comments-container", "children"),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('channel-id', 'value')]
)
def update_comments(n_clicks, channel_id):
    if n_clicks > 0:
        # Fetch video comments (you need to change the video_id to the latest video id)
        comments = get_video_comments("SV01PfG5LIA")
        return [html.P(comment) for comment in comments]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
