import pymongo
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from wordcloud import WordCloud

client = pymongo.MongoClient(
    "mongodb+srv://sma_admin:nDoOqwGU4z2dBTJP@smacluster.ikhoi.mongodb.net/?retryWrites=true&w=majority&appName=smacluster"
)
db = client["youtubedata"]

videos_collection = db["video"]
videos_data = list(videos_collection.find())

likes_by_month = defaultdict(int)
comments_by_month = defaultdict(int)
views_by_month = defaultdict(int)

for video in videos_data:
    published_at = datetime.strptime(video["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    month_key = published_at.strftime("%Y-%m")
    likes_by_month[month_key] += int(video["likes"])
    comments_by_month[month_key] += int(video["totalComments"])
    views_by_month[month_key] += int(video["views"])

sorted_likes_by_month = dict(sorted(likes_by_month.items()))
sorted_comments_by_month = dict(sorted(comments_by_month.items()))
sorted_views_by_month = dict(sorted(views_by_month.items()))

months = list(sorted_likes_by_month.keys())

combined_text = ""
for video in videos_data:
    combined_text += video["title"] + " " + video["description"] + " "

# For the first chart; likes vs comments over time

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(
    months,
    list(sorted_likes_by_month.values()),
    marker="o",
    color="b",
    label="Cumulative Likes",
)
ax1.set_xlabel("Month")
ax1.set_ylabel("Cumulative Likes", color="b")
ax1.tick_params("y", colors="b")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(
    months,
    list(sorted_comments_by_month.values()),
    marker="o",
    color="r",
    label="Cumulative Comments",
)
ax2.set_ylabel("Cumulative Comments", color="r")
ax2.tick_params("y", colors="r")

# For the second chart; views over time

fig2, ax3 = plt.subplots(figsize=(10, 6))

ax3.plot(
    months,
    list(sorted_views_by_month.values()),
    marker="o",
    color="g",
    label="Cumulative Views",
)
ax3.set_xlabel("Month")
ax3.set_ylabel("Cumulative Views", color="g")
ax3.tick_params("y", colors="g")
ax3.grid(True)

plt.title("Cumulative Likes, Comments, and Views by Month for Top 10 Videos")
plt.xticks(rotation=45, ha="right")

fig.tight_layout()
fig2.tight_layout()

# For the third chart; a wordcloud of the text components of the data (title and description)

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
    combined_text
)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

client.close()
