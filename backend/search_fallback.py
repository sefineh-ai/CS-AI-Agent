import requests
from config import Config

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": Config.GOOGLE_CSE_ID,
        "key": Config.GOOGLE_API_KEY,
        "num": 3
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    return [item["snippet"] for item in data.get("items", [])]
