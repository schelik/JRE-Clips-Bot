import requests
from IPython.display import HTML
import json
import os
from dotenv import load_dotenv

load_dotenv()
subscription_key = os.getenv("subscription_key")
assert subscription_key
search_url = "https://api.bing.microsoft.com/v7.0/images/search"
search_term = "dogs"
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
params = {
    "q": search_term,
}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

with open("bing.txt", "w") as file:
    json.dump(search_results, file)
