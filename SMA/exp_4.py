import pymongo
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from collections import defaultdict
from datetime import datetime
from wordcloud import WordCloud

client = pymongo.MongoClient(
    "mongodb+srv://sma_admin:nDoOqwGU4z2dBTJP@smacluster.ikhoi.mongodb.net/?retryWrites=true&w=majority&appName=smacluster"
)
db = client["youtubedata"]

videos_collection = db["video"]
videos_data = list(videos_collection.find())

likes_by_month = defaultdict(lambda: defaultdict(int))
comments_by_month = defaultdict(lambda: defaultdict(int))
views_by_month = defaultdict(lambda: defaultdict(int))

video_names = []  # To store video names

for video in videos_data:
    published_at = datetime.strptime(video["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    month_key = published_at.strftime("%Y-%m")
    likes_by_month[video["title"]][month_key] += int(video["likes"])
    comments_by_month[video["title"]][month_key] += int(video["totalComments"])
    views_by_month[video["title"]][month_key] += int(video["views"])
    video_names.append(video["title"])

# Extract unique months
months = sorted(set(month for video_data in likes_by_month.values() for month in video_data.keys()))

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

for video_name, likes_data in likes_by_month.items():
    ax1.plot(
        months,
        [likes_data[month] for month in months],
        marker="o",
        label=f"{video_name} - Likes"
    )

ax1.set_xlabel("Month")
ax1.set_ylabel("Cumulative Likes")
ax1.grid(True)
plt.xticks(rotation=45, ha="right")
ax1.legend(loc="upper left")

ax2 = ax1.twinx()

for video_name, comments_data in comments_by_month.items():
    ax2.plot(
        months,
        [comments_data[month] for month in months],
        marker="o",
        label=f"{video_name} - Comments"
    )

ax2.set_ylabel("Cumulative Comments")
ax2.legend(loc="upper right")

fig.tight_layout()

# Setting a font that includes the necessary glyphs
plt.rcParams['font.family'] = 'DejaVu Sans'

# Wordcloud
combined_text = ""
for video in videos_data:
    combined_text += video["title"] + " " + video["description"] + " "

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(combined_text)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

client.close()
