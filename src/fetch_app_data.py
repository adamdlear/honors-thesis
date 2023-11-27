"""
To find examples for research, I wanted to scrape Apple App Store data.
By pulling transportation-themed mobile apps I could easily find which apps have high and low user ratings.
This may indicate which apps will be suitable for examples of well and poorly designed mobile apps.

To get this data I used the "App Store Data Extractor" on APIFY (https://apify.com/epctex/appstore-scraper).
"""

# pip install apify_client

from sqlalchemy.sql.expression import true
from apify_client import ApifyClient
import json

# Initialize token constant
# TOKEN = ...

# Initialize the ApifyClient with your API token
client = ApifyClient(TOKEN)

# Prepare the Actor input
run_input = {
    "country": "us",
    "customMapFunction": "(object) => { return {...object} }",
    "includeReviews": False,
    "maxItems": 1000,
    "mediaType": "software",
    "mode": "search",
    "proxy": {
        "useApifyProxy": True
    },
    "term": "transportation"
}

# Run the Actor and wait for it to finish
run = client.actor("epctex/appstore-scraper").call(run_input=run_input)
# Output can be found on and downloaded from ApifyClient page

# Load in API output from preivous step
data = pd.read_csv('api-output.csv')

# Clean and filter data
data = data.drop_duplicates()
data = data[(data['primaryGenreName'] == 'Travel') | (data['primaryGenreName'] == 'Navigation')]
data = data[data['userRatingCount'] >= 100]

# Export data to CSV
data.to_csv('transportation-data.csv')