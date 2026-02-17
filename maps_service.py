import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_nearby_places(lat, lng, keyword):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,
        "keyword": keyword,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []

    for place in data.get("results", [])[:5]:
        results.append({
            "name": place.get("name"),
            "rating": place.get("rating", "N/A"),
            "address": place.get("vicinity"),
            "location": place["geometry"]["location"]
        })

    return results
