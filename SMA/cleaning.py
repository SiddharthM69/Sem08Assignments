import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load the CSV file
csv_file = "comments.csv"
df = pd.read_csv(csv_file)

# Display the first few rows of the dataframe
print("Before cleaning:")
print(df.head())

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.dropna(inplace=True)


# Function to clean the text
def clean_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    # Remove special characters and punctuation
    text = re.sub(r"[^\w\s]", "", text)
    # Remove numbers
    text = re.sub(r"\d+", "", text)
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Join the tokens back into text
    cleaned_text = " ".join(filtered_tokens)
    return cleaned_text


# Apply the clean_text function to the 'comment_text' column
df["cleaned_comment"] = df["comment_text"].apply(clean_text)

# Display the first few rows of the cleaned dataframe
print("\nAfter cleaning:")
print(df.head())
json_data = df.to_json(orient="records")

# Print or save the JSON data
print(json_data)

# If you want to save it to a JSON file
json_file = "cleaned_youtube_comments.json"
# Save the cleaned dataframe to a new CSV file
with open(json_file, "w") as f:
    f.write(json_data)
cleaned_csv_file = "cleaned_youtube_comments.csv"
df.to_csv(cleaned_csv_file, index=False)

print(f"\nCleaned data saved to {cleaned_csv_file}")

