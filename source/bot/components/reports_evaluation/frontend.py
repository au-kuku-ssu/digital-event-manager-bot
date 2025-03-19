from aiogram import Bot, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")

async def frontend_cb_re_main(callback_query: types.CallbackQuery, bot: Bot) -> None:
  lang = "ru"

  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, "reports_evaluation.main.back"), callback_data="cb_mm_main")

  keyboard.adjust(1)

  await callback_query.message.edit_text(getstr(lang, "reports_evaluation.main.caption"), reply_markup=keyboard.as_markup())