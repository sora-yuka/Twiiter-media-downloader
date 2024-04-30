from aiogram import Router, types
from aiogram.filters import CommandStart

from .twitter_handler import extract_tweet_id, reply_media
from utilities.extractor import scrape_media, scrape_user_name

router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message) -> None:
    user = message.from_user.mention_markdown()
    await message.delete()
    await message.answer(
        text=f"Hi {user}\n"
        + "Send me tweet url, and I'll send you media in best available quality."
    )
    
@router.message()
async def handle_message(message: types.Message) -> None:
    """Handling twitter content from user message"""
    found_media = False
    found_tweet = False
    
    tweet_ids = await extract_tweet_id(message)
    
    try:
        for tweet_id in tweet_ids:
            found_tweet = True
            media = scrape_media(tweet_id)
            owner = scrape_user_name(tweet_id)
            
            if media:
                if await reply_media(message, media, owner):
                    found_media = True
            else:
                await message.reply("Tweet has no media")
    except TypeError:
        pass