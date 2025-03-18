from aiogram import Bot, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

pr_router = Router()

@pr_router.callback_query(lambda c: c.data == "cb_pr_main")
async def cb_pr_main_menu(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Регистрация участника", callback_data="cb_locale_ru")
    keyboard.button(text="Жеребьевка", callback_data="cb_locale_en")

    keyboard.adjust(1)

    await callback_query.message.edit_text("Выберите опцию", reply_markup=keyboard.as_markup())