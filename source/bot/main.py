import asyncio
import logging
import sys
import os

from os.path import join, dirname
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.main_menu.component import main_menu_router
from components.participant_registration.component import pr_router

async def main() -> None:
    """
    Main function to run the bot.
    """

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    load_dotenv(join(dirname(__file__), '..', '.env'))

    bot = Bot(token=os.environ.get("TG_BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(main_menu_router)
    dp.include_router(pr_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
