import csv
import os
import praw
from dotenv import load_dotenv

load_dotenv()

def harvest_reddit_reviews(subreddit_name, search_query, max_submissions=10):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    subreddit = reddit.subreddit(subreddit_name)
    harvested_data = []
    row_id = 0

    print(f"Scanning r/{subreddit_name} looking for references matching: '{search_query}'...")

    for submission in subreddit.search(search_query, limit=max_submissions):
        print(f"Processing Thread ID: {submission.id} - Title: {submission.title}")

        if submission.selftext and len(submission.selftext) > 20:
            harvested_data.append({
                "ID": row_id,
                "Reviews": submission.selftext.replace('\n', ' ').strip(),
                "Sentiment": ""
            })
            row_id += 1

        submission.comments.replace_more(limit=0)  # Drop deeply nested "load more comments" nodes for safety
        for comment in submission.comments.list():
            if len(comment.body) > 15:
                harvested_data.append({
                    "ID": row_id,
                    "Reviews": comment.body.replace('\n', ' ').strip(),
                    "Sentiment": ""
                })
                row_id += 1

    return harvested_data


def save_to_csv(data, output_filepath):
    fieldnames = ["ID", "Reviews", "Sentiment"]
    with open(output_filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Reddit structured matrix saved: {output_filepath}")


if __name__ == "__main__":
    SUBREDDIT = "assam"
    QUERY = "Assamese movie review"
    OUTPUT_FILE = "Reddit_Harvest_Raw.csv"

    results = harvest_reddit_reviews(SUBREDDIT, QUERY, max_submissions=10)
    save_to_csv(results, OUTPUT_FILE)