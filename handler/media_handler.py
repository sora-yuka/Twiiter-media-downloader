import time
from typing import List, Dict
from os.path import basename

import requests
from requests.exceptions import RequestException
from tempfile import TemporaryFile

from aiogram import Router, types
from aiogram.types import URLInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.exceptions import TelegramBadRequest


router = Router()

@router.message()
async def reply_gif(
        message: types.Message,
        tweet_gif: List[Dict[str, str]],
        tweet_owner: str) -> None:
    await message.reply_animation(
        animation=tweet_gif[0]["url"],
        caption=f"Gif from {tweet_owner}'s tweet",
    )

@router.message()
async def reply_photo(
        message: types.Message, 
        tweet_photos: List[Dict[str, str]], 
        tweet_owner: str) -> None:
    photo_group = MediaGroupBuilder(caption=f"Made by {tweet_owner}")
    photo_url = tweet_photos[0]["url"]
    
    if len(tweet_photos) == 1:
        await message.reply_document(
            document=URLInputFile(url=photo_url, filename=basename(photo_url)),
            caption=f"Mady by {tweet_owner}"
        )
    else:
        for photo in tweet_photos:
            photo_group.add(type="photo", media=photo["url"])
        await message.bot.send_media_group(
            chat_id=message.from_user.id, 
            media=photo_group.build(),
        )
    
@router.message()
async def reply_video(
        message: types.Message,
        tweet_video: List[Dict[str, str]],
        tweet_owner: str) -> None:
    video_url = tweet_video[0]["url"]
    
    try:
        request = requests.get(video_url, stream=True)
        request.raise_for_status()
        
        if (video_size := int(request.headers["Content-length"])) <= int(20e6):
            await message.answer("Preparing for sending. Please wait...")
            time.sleep(3)
            
            await message.reply_video(
                video=video_url,
                caption=f"Made by {tweet_owner}",
            )
        elif video_size <= 50e6:
            await message.reply("File bigger that expected. Please wait a bit long...")
            time.sleep(3)
            
            await message.reply_document(
                document=URLInputFile(
                    url=video_url,
                    filename=basename(video_url.split("?")[0]),
                ),
                caption=f"Made by {tweet_owner}",
            )
        else:
            await message.reply(
                text="Video is too large for Telegram. Use direct link to download:\n"
                + video_url
            )
    except(requests.HTTPError, KeyError, TelegramBadRequest, RequestException) as exception:
        await message.reply(
            f"Error occurred when trying to send video. Use direct link:\n{video_url}")
        print(exception)