import asyncio
import logging
import os
import sys

from os.path import join, dirname
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import components.main_menu.router as main_menu
import components.participant_drawer.router as participant_drawer
import components.participant_registration.router as participant_registration
import components.program_generator.router as program_generator
import components.reports_evaluation.router as reports_evaluation

from components.shared.db import Database
from middlewares.db import DatabaseMiddleware


async def main() -> None:
    """
    Main function to run the bot.
    """

    dotenv_dir = join(dirname(__file__), "..", ".env")

    component_routers = [
        main_menu.router,
        participant_drawer.router,
        participant_registration.router,
        program_generator.router,
        reports_evaluation.router,
    ]

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    load_dotenv(dotenv_dir)

    db_path = join(dirname(__file__), "database", "instance", "digital_event_manager.db")
    db = Database(db_path).connect()

    bot = Bot(
        token=os.getenv("TG_BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    dp.message.middleware(DatabaseMiddleware(db))
    dp.callback_query.middleware(DatabaseMiddleware(db))

    dp.include_routers(*component_routers)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
