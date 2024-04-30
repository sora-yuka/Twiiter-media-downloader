from typing import List, Optional, List, Dict

import re
import requests
from aiogram.types import update


url = "https://api.vxtwitter.com/Twitter/status/"

def scrape_media(tweet_id: int) -> List[dict]:
    """Scraping media list from twitter api"""
    request = requests.get(url + tweet_id)
    request.raise_for_status()
    return request.json()["media_extended"]

def scrape_user_name(tweet_id: int) -> str:
    """Scraping tweet owner username from twitter api"""
    request = requests.get(url + tweet_id)
    request.raise_for_status()
    return request.json()["user_name"]

def extract_link(tweet_url: str) -> Optional[List[Dict[str, str]]]:
    """Extracting id from tweet url"""
    unshortened_links = ""
    
    for link in re.findall(r"t\.co\/[a-zA-Z0-9]+", tweet_url):
        unshortened_link = requests.get("https://" + link).url
        unshortened_links += "\n" + unshortened_link
        
    tweet_id = re.findall(
        r"(?:twitter|x)\.com/.{1,15}/(?:web|status(?:es)?)/([0-9]{1,20})", 
        tweet_url + unshortened_links,
    )
    tweet_id = list(dict.fromkeys(tweet_id))
    return tweet_id or None