from telethon import events
from serpapi import GoogleSearch
import configparser

# Load configurations
config = configparser.ConfigParser()
config.read('config.ini')
SERPAPI_KEY = config.get('default', 'serpapi_key')

async def web_search(event):
    await event.respond("🔍 Enter your search query:")

async def fetch_results(event):
    search_query = event.text
    
    # Call SerpAPI
    params = {
        "q": search_query,
        "api_key": SERPAPI_KEY,
        "num": 3
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract search results
    if "organic_results" in results:
        summary = "\n".join([f"{res['title']}: {res['link']}" for res in results["organic_results"][:3]])
        response = f"🔎 Search Results:\n{summary}"
    else:
        response = "❌ No results found."

    await event.respond(response)
