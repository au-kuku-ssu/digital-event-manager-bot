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

load_dotenv(join(dirname(__file__), '..', '.env'))

bot = Bot(token=os.environ.get("TG_BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with /start command.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Русский (RU)", callback_data="cb_locale_ru")
    keyboard.button(text="Английский (EN)", callback_data="cb_locale_en")

    await message.answer("Выберите язык / Choose language", reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data == "cb_locale_ru")
async def callback_russian_language(callback_query: types.CallbackQuery):
    await callback_main_menu(callback_query)

@dp.callback_query(lambda c: c.data == "cb_locale_en")
async def callback_english_language(callback_query: types.CallbackQuery):
    await callback_main_menu(callback_query)

async def callback_main_menu(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Регистрация участника", callback_data="cb_locale_ru")
    keyboard.button(text="Жеребьевка", callback_data="cb_locale_en")
    keyboard.button(text="Оценка докладов", callback_data="cb_locale_en")
    keyboard.button(text="Генерация программы мероприятия", callback_data="cb_locale_en")
    keyboard.button(text="Настройки", callback_data="cb_locale_en")
    keyboard.adjust(1)

    await callback_query.message.edit_text("Выберите опцию", reply_markup=keyboard.as_markup())

async def main() -> None:
    """
    Main function to run the bot.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
