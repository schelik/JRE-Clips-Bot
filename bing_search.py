import requests
from IPython.display import HTML
import json
import os
import time
from dotenv import load_dotenv
from slugify import slugify
from PIL import Image

load_dotenv()


def download_thumbnail_image(chapter):
    subscription_key = os.getenv("subscription_key")
    assert subscription_key
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    search_term = chapter.title
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {
        "q": search_term,
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = json.loads(response.content)
    image_url = search_results["value"][0]["contentUrl"]
    print(search_results["value"][0]["contentUrl"])
    print(search_results["value"][0]["hostPageUrl"])
    image_credit_url = search_results["value"][0]["hostPageUrl"]
    image_response = requests.get(image_url)
    time.sleep(60)

    chapter.description += "Thumbnail image credit: " + image_credit_url + "\n"
    chapter.thumnail_image_file_name = (
        slugify(chapter.title + "-thumbnail-picture") + ".jpg"
    )
    with open(chapter.thumnail_image_file_name, "wb") as handler:
        handler.write(image_response.content)
    time.sleep(10)
