from aiogram import Bot, Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "..", "locale"))
getstr = lambda lang, prefix, path: get_locale_str(locale, f"{lang}.{prefix}.{path}")

async def pr_cb_user_browse(callback_query: types.CallbackQuery, bot: Bot) -> None:
  lang = "ru"
  prefix = "participant_registration.user.browse"
  shared = "participant_registration.shared"

  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "left"), callback_data="idk")
  keyboard.button(text=getstr(lang, shared, "right"), callback_data="idk")
  keyboard.button(text=getstr(lang, prefix, "register"), callback_data="pr_cb_user_register")
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  keyboard.adjust(2, 1, 1)

  await callback_query.message.edit_text("Placeholder", reply_markup=keyboard.as_markup())

