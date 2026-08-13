#YouTube Data API scraper template
import csv
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

def harvest_youtube_comments(video_id, max_results=100):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY not found in .env")

    youtube = build("youtube", "v3", developerKey=api_key)

    comments_data = []
    row_id = 0
    next_page_token = None

    print(f"Starting comment harvest for YouTube video: {video_id}...")

    while len(comments_data) < max_results:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_results - len(comments_data)),
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response.get("items", []):
                comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comment_text = comment_text.replace("\n", " ").strip()

                if len(comment_text) > 10:
                    comments_data.append({
                        "ID": row_id,
                        "Reviews": comment_text,
                        "Sentiment": ""  # Left unassigned for manual/double annotator alignment
                    })
                    row_id += 1

            next_page_token = response.get("nextPageToken")
            print(f"Harvested {len(comments_data)} comments so far...")

            if not next_page_token:
                print("End of comment stream reached.")
                break

        except Exception as e:
            print(f"Error during runtime loop: {str(e)}")
            break

    return comments_data


def save_to_csv(data, output_filepath):
    fieldnames = ["ID", "Reviews", "Sentiment"]
    with open(output_filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data file written successfully: {output_filepath}")


if __name__ == "__main__":
    TARGET_VIDEO_ID = "dQw4w9WgXcQ"  # Substitute with real target ID (from video URL: youtube.com/watch?v=VIDEO_ID)
    OUTPUT_FILE = "YouTube_Harvest_Raw.csv"

    extracted_comments = harvest_youtube_comments(TARGET_VIDEO_ID, max_results=50)
    save_to_csv(extracted_comments, OUTPUT_FILE)