from aiogram import Bot, Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "..", "locale"))
getstr = lambda lang, prefix, path: get_locale_str(locale, f"{lang}.{prefix}.{path}")

async def pr_cb_pre_main(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()

  keyboard.button(text="Участник", callback_data="pr_cb_user_main")
  keyboard.button(text="Администратор", callback_data="pr_cb_admin_main")

  await callback_query.message.edit_text("[DEBUG] Выберите роль", reply_markup=keyboard.as_markup())

async def pr_cb_user_main(callback_query: types.CallbackQuery, bot: Bot) -> None:
  lang = "ru"
  prefix = "user_registration.user.main"

  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, prefix, "browse"), callback_data="pr_cb_user_register")
  keyboard.button(text=getstr(lang, prefix, "search"), callback_data="pr_cb_user_show")
  keyboard.button(text=getstr(lang, prefix, "my_activities"), callback_data="pr_cb_user_activities")
  keyboard.button(text=getstr(lang, prefix, "my_data"), callback_data="pr_cb_user_activities")
  keyboard.button(text=getstr(lang, prefix, "back"), callback_data="cb_mm_main")

  keyboard.adjust(1)

  await callback_query.message.edit_text(getstr(lang, prefix, "caption"), reply_markup=keyboard.as_markup())

