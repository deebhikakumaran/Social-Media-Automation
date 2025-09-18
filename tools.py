import os
import gspread
from langchain.tools import tool
from firecrawl import Firecrawl
from typing import Optional
from dotenv import load_dotenv
import requests
import tweepy

load_dotenv() 

firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

@tool
def get_article_url(sheet_name: str, link_column: str) -> Optional[str]:
    """
    Fetches the single latest news media link from the last row of a specified Google Sheet.
    The sheet must have a column for the links.
    """
    try:
        gc = gspread.service_account(filename="credentials.json")
        worksheet = gc.open(sheet_name).sheet1
        col_index = worksheet.find(link_column).col
        links = worksheet.col_values(col_index)

        if not links or len(links) <= 1:
            print("No links found or only a header row exists.")
            return None
        
        # Get the latest URL (last row) and its 1-based row index
        latest_url = links[-1]
        row_number = len(links) 

        return latest_url, row_number
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet '{sheet_name}' not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
@tool
def scrape_article(url: str) -> Optional[str]:
    """
    Scrapes the content of a single URL using the FirecrawlScrapeTool.
    """
    try:
        print(f"Scraping URL: {url}")
        content = firecrawl.scrape(
            url,
            formats=["markdown"]
        )
        print("Scraping successful.")
        return content
    except Exception as e:
        print(f"An error occurred while scraping: {e}")
        return None

@tool
def post_to_twitter(tweet_content: str):
    """Posts content to Twitter (X)."""
    try:
        consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            raise ValueError("Twitter API credentials are not set.")

        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        api = tweepy.API(auth)
        api.update_status(tweet_content)
        print("Successfully posted to Twitter.")
        return "Posted"
    except Exception as e:
        print(f"Failed to post to Twitter: {e}")
        return f"Post failed: {e}"

@tool
def post_to_linkedin(post_content: str):
    """Posts content to LinkedIn."""
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    company_id = os.getenv("LINKEDIN_COMPANY_ID") 

    if not access_token or not company_id:
        return "Post failed: Missing credentials."
    
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "author": f"urn:li:person:{os.getenv('LINKEDIN_PERSON_URN')}", 
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        id = response.json().get("id", "N/A")
        print(f"Post ID: {id}")
        return "Posted."
    except requests.exceptions.HTTPError as err:
        print(f"Response: {response.text}")
        return f"Post failed: {err}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Post failed: {e}"
    
@tool
# def update_google_sheet(sheet_name: str, link_column: str, row_index: int, linkedin_content: str, twitter_content: str, linkedin_status: str, twitter_status: str):
def update_google_sheet(sheet_name: str, link_column: str, row_index: int, linkedin_content: str, linkedin_status: str):
    """Updates a row in a Google Sheet with post content and status."""
    try:
        gc = gspread.service_account(filename="credentials.json")
        worksheet = gc.open(sheet_name).sheet1

        # Assuming columns for content and status are defined
        headers = worksheet.row_values(1)
        linkedin_col_index = headers.index("LinkedIn Content") + 1
        # twitter_col_index = headers.index("Twitter Content") + 1
        linkedin_status_col_index = headers.index("LinkedIn Status") + 1
        # twitter_status_col_index = headers.index("Twitter Status") + 1

        worksheet.update_cell(row_index, linkedin_col_index, linkedin_content)
        # worksheet.update_cell(row_index, twitter_col_index, twitter_content)
        worksheet.update_cell(row_index, linkedin_status_col_index, linkedin_status)
        # worksheet.update_cell(row_index, twitter_status_col_index, twitter_status)
        print(f"Successfully updated row {row_index + 1} in Google Sheet.")
        return "Sheet updated successfully"
    except Exception as e:
        print(f"Failed to update Google Sheet: {e}")
        return f"Sheet update failed: {e}"
