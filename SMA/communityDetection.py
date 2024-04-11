import pandas as pd
import warnings
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# Load dataset
dataset = pd.read_csv("tweets.csv")

# Filter dataset and preprocess hashtags
dataset = dataset[dataset.user_location.notnull()][:10]
dataset["hashtags"] = ""

for i, row in dataset.iterrows():
    hashtags = [token for token in row.tweet.split() if token.startswith("#")]
    dataset.at[i, "hashtags"] = hashtags

# Explode dataset to separate rows for each hashtag
dataset = dataset.explode("hashtags")
users = list(dataset["user"].unique())
hashtags = list(dataset["hashtags"].unique())

# Create a graph
vis = nx.Graph()
vis.add_nodes_from(users + hashtags)

# Add edges between users and hashtags
for name, group in dataset.groupby(["hashtags", "user"]):
    hashtag, user = name
    weight = len(group)
    vis.add_edge(hashtag, user, weight=weight)

# Community Detection
community_gen = community.girvan_newman(vis)
top_level_communities = next(community_gen)

# Extract communities
communities = list(next(community_gen))

# Print communities
print("Detected Communities:", communities)

# Visualize the graph
plt.figure(figsize=(8, 8))
nx.draw(vis, with_labels=True, node_color="skyblue", node_size=300, font_size=10)
plt.title("Network Graph of Users and Hashtags")
plt.axis("off")
plt.show()

# Analyze influential nodes
centrality = nx.betweenness_centrality(vis)
print("Top 5 Influential Users/Hashtags:")
influential_nodes = sorted(centrality.items(), key=lambda item: item[1], reverse=True)[
    :5
]

for nodes in influential_nodes:
    print(f"{nodes[0]} has centrality of {nodes[1]}")

