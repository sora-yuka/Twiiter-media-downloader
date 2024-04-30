from typing import Optional, List, Dict

import re
import requests
from urllib.parse import urlsplit
from aiogram import Router, types

from .media_handler import reply_gif, reply_video, reply_photo
from utilities.extractor import extract_link

router = Router()

@router.message()
async def extract_tweet_id(message: types.Message) -> Optional[List[Dict[str, str]]]:
    """Extracting tweet id from user message"""
    url = message.text
    
    try:
        return extract_link(url) or None
    except Exception as e:
        await message.reply("Couldn't unshortened link.")
        
@router.message()
async def reply_media(
        message: types.Message,
        tweet_media: List[Dict[str, str]],
        tweet_owner: str) -> bool:
    """Preparing content to answer"""
    photos = [media for media in tweet_media if tweet_media[0]["type"] == "image"]
    videos = [media for media in tweet_media if tweet_media[0]["type"] == "video"]
    gifs = [media for media in tweet_media if tweet_media[0]["type"] == "gif"]
    
    if photos:
        await reply_photo(message, photos, tweet_owner)
    if videos:
        await reply_video(message, videos, tweet_owner)
    if gifs:
        await reply_gif(message, gifs, tweet_owner)