from aiogram import Bot, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_menu_router = Router()

@main_menu_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with /start command.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Русский (RU)", callback_data="cb_locale_ru")
    keyboard.button(text="Английский (EN)", callback_data="cb_locale_en")

    await message.answer("Выберите язык / Choose language", reply_markup=keyboard.as_markup())

@main_menu_router.callback_query(lambda c: c.data == "cb_locale_ru")
async def callback_russian_language(callback_query: types.CallbackQuery):
    await callback_main_menu(callback_query)

@main_menu_router.callback_query(lambda c: c.data == "cb_locale_en")
async def callback_english_language(callback_query: types.CallbackQuery):
    await callback_main_menu(callback_query)

async def callback_main_menu(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Регистрация участника", callback_data="cb_pr_main")
    keyboard.button(text="Жеребьевка", callback_data="cb_locale_en")
    keyboard.button(text="Оценка докладов", callback_data="cb_locale_en")
    keyboard.button(text="Генерация программы мероприятия", callback_data="cb_locale_en")
    keyboard.button(text="Настройки", callback_data="cb_locale_en")
    keyboard.adjust(1)

    await callback_query.message.edit_text("Выберите опцию", reply_markup=keyboard.as_markup())