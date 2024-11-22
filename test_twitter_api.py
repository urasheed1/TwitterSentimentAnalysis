import os
import requests
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()

# Fetch the BEARER_TOKEN from .env
bearer_token = os.getenv("BEARER_TOKEN")

# Verify that the token is loaded
if not bearer_token:
    print("Error: Bearer token not found. Make sure it's set in the .env file.")
    exit(1)

# Define the API endpoint and headers
url = "https://api.twitter.com/2/tweets/search/recent"
headers = {
    "Authorization": f"Bearer {bearer_token}",
}

# Define query parameters
params = {
    "query": "python",  # Replace with your search term
    "max_results": 10   # Must be between 10 and 100
}

# Function to make the API call with retry logic
def fetch_tweets():
    for attempt in range(3):  # Retry up to 3 times
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            # Successfully fetched tweets
            tweets = response.json()
            print("API Connection Successful. Recent Tweets:")
            for tweet in tweets.get("data", []):
                print(f"- {tweet['text']}")
            return
        elif response.status_code == 429:
            # Rate limit hit, wait and retry
            print("Rate limit exceeded. Waiting for reset...")
            time.sleep(60)  # Wait for 1 minute before retrying
        else:
            # Other errors
            print("API Request Failed.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return
    print("Failed to fetch tweets after 3 attempts.")

# Call the function
fetch_tweets()
