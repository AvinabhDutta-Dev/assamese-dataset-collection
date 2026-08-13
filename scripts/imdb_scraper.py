import csv
import time
import requests
from bs4 import BeautifulSoup

def scrape_imdb_reviews(movie_id, max_results=100):
    url = f"https://www.imdb.com/title/{movie_id}/reviews/_ajax"
    params = {
        "ref_": "undefined",
        "paginationKey": ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    reviews_data = []
    row_id = 0

    print(f"Starting data harvest for IMDb Title: {movie_id}...")

    while len(reviews_data) < max_results:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code != 200:
                print(f"HTTP Connection Warning: Status code {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            review_containers = soup.find_all('div', class_='review-container')

            if not review_containers:
                print("End of review stream reached or pagination structural shift.")
                break

            for container in review_containers:
                if len(reviews_data) >= max_results:
                    break

                text_div = container.find('div', class_='text show-more-__control')
                if not text_div:
                    text_div = container.find('div', class_='text')

                if text_div:
                    review_text = text_div.get_text(strip=True)

                    reviews_data.append({
                        "ID": row_id,
                        "Reviews": review_text,
                        "Sentiment": ""  # Left unassigned for subsequent manual/double annotator alignment
                    })
                    row_id += 1

            load_more_data = soup.find('div', class_='load-more-data')
            if load_more_data and load_more_data.has_attr('data-key'):
                params['paginationKey'] = load_more_data['data-key']
            else:
                break

            print(f"Harvested {len(reviews_data)} inputs successfully...")
            time.sleep(1.5)  # Strict defensive rate-limiting constraint

        except Exception as e:
            print(f"Error during runtime loop: {str(e)}")
            break

    return reviews_data


def save_to_csv(data, output_filepath):
    fieldnames = ["ID", "Reviews", "Sentiment"]
    with open(output_filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data file written successfully: {output_filepath}")


if __name__ == "__main__":
    TARGET_MOVIE = "tt11124312"  # Substitute with real target ID (from IMDb URL: imdb.com/title/tt.../)
    OUTPUT_FILE = "Imdb_Harvest_Raw.csv"

    extracted_reviews = scrape_imdb_reviews(TARGET_MOVIE, max_results=50)
    save_to_csv(extracted_reviews, OUTPUT_FILE)