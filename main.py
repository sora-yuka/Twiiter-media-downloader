import sys
import logging
import asyncio
from os import makedirs
from decouple import config

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handler import router as main_router

async def on_startup() -> None:
    print("Bot has been startup!")

async def main() -> None:
    makedirs("data", exist_ok=True)
    
    dispatcher = Dispatcher()
    bot = Bot(
        config("TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    
    dispatcher.include_router(main_router)
    dispatcher.startup.register(on_startup)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filemode="a+", filename="./data/bot.log",
                        format=("TIME: %(asctime)s | LEVEL: %(levelname)s | MESSAGE: %(message)s"))
    asyncio.run(main())