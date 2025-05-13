import asyncio
import logging
import os
import sys
from os.path import join, dirname

import logging_loki
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import components.main_menu.router as main_menu
import components.participant_drawer.router as participant_drawer
import components.participant_registration.router as participant_registration
import components.program_generator.router as program_generator
import components.reports_evaluation.router as reports_evaluation


async def main() -> None:
  # Ensure the /var/log directory exists
  os.makedirs('/var/log', exist_ok=True)

  # Set up logger
  logger = logging.getLogger("app_logger")
  logger.setLevel(logging.INFO)

  # Create a file handler for local logs
  file_handler = logging.FileHandler('/var/log/app_logger.log')
  file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(file_formatter)
  logger.addHandler(file_handler)

  # Set up Loki handler
  loki_handler = logging_loki.LokiHandler(
    url="http://loki:3100/loki/api/v1/push",  # Адрес Loki сервера
    tags={"application": "telegram-bot"},
    version="1",
  )

  # Добавляем обработчик для отправки логов в Loki
  logger.addHandler(loki_handler)

  # Логируем старт приложения
  logger.info("Application started", extra={
    "service": "telegram-bot",
    "version": "1.0.0",
    "environment": os.getenv("ENVIRONMENT", "development")
  })

  dotenv_dir = join(dirname(__file__), "..", "../.env")
  component_routers = [
    main_menu.router,
    participant_drawer.router,
    participant_registration.router,
    program_generator.router,
    reports_evaluation.router,
  ]

  # Настраиваем корневой логгер для всех модулей
  logging.basicConfig(level=logging.INFO, handlers=[loki_handler, file_handler])

  load_dotenv(dotenv_dir)

  # Используем переменную окружения для токена бота
  bot_token = "NEED TO GAIN TOKEN HERE"

  '''(os.getenv("TG_BOT_TOKEN"))'''

  bot = Bot(
    token=bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
  )
  dp = Dispatcher()

  dp.include_routers(*component_routers)

  logger.info("Bot polling started")
  try:
    await dp.start_polling(bot)
  except Exception as e:
    logger.error(f"Error during bot execution: {e}", exc_info=True)


if __name__ == "__main__":
  asyncio.run(main())
