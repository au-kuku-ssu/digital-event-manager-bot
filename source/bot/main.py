import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder  # Better for inline keyboards

from components.shared.utilities import get_env_data_as_dict

TOKEN = get_env_data_as_dict(".env")["TG_BOT_TOKEN"]
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with /start command.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Русский (RU)", callback_data="button1")
    keyboard.button(text="Английский (EN)", callback_data="button2")

    await message.answer("Выберите язык / Choose language", reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data == "button1")
async def callback_russian_language(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("🔘 Вы нажали кнопку 1!")

@dp.callback_query(lambda c: c.data == "button2")
async def callback_english_language(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("🔘 Вы нажали кнопку 2!")

async def main() -> None:
    """
    Main function to run the bot.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
