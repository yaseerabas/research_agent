import requests
from bs4 import BeautifulSoup
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def get_web_results(query):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"q": query}

    resp = requests.post(url, json=payload, headers=headers)
    data = resp.json()
    return [item['link'] for item in data.get("organic", [])[:5]]

def scrape_text_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        return "\n".join([p.text for p in soup.find_all("p")])
    except:
        return ""

