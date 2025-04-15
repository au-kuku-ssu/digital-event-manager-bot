from aiogram import Bot, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")

async def frontend_cmd_mm_start(message: Message, bot: Bot) -> None:
  """
  This handler receives messages with /start command.
  """
  keyboard = InlineKeyboardBuilder()

  keyboard.button(text="Русский 🇷🇺", callback_data="cb_locale_ru")
  keyboard.button(text="Английский 🇬🇧", callback_data="cb_locale_en")

  await message.answer("Выберите язык / Choose language", reply_markup=keyboard.as_markup())

async def frontend_cb_mm_main(callback_query: types.CallbackQuery, bot: Bot) -> None:
  lang = "ru"

  keyboard = InlineKeyboardBuilder()

  keyboard.button(text=getstr(lang, "main_menu.main.register"), callback_data="pr_cb_pre_main")
  keyboard.button(text=getstr(lang, "main_menu.main.draw"), callback_data="cb_pd_main")
  keyboard.button(text=getstr(lang, "main_menu.main.reports_evaluation"), callback_data="cb_re_main")
  keyboard.button(text=getstr(lang, "main_menu.main.program_generation"), callback_data="cb_pg_main")
  keyboard.button(text=getstr(lang, "main_menu.main.settings"), callback_data="cb_mm_settings")

  keyboard.adjust(1)

  await callback_query.message.edit_text(getstr(lang, "main_menu.main.caption"), reply_markup=keyboard.as_markup())

async def frontend_cb_mm_settings(callback_query: types.CallbackQuery, bot: Bot) -> None:
  lang = "ru"

  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, "main_menu.settings.back"), callback_data="cb_mm_main")

  keyboard.adjust(1)

  await callback_query.message.edit_text(getstr(lang, "main_menu.settings.caption"), reply_markup=keyboard.as_markup())