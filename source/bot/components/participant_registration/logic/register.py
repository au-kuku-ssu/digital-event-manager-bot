from aiogram import Bot, Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "..", "locale"))
getstr = lambda lang, prefix, path: get_locale_str(locale, f"{lang}.{prefix}.{path}")

lang = "ru"
prefix_base = "participant_registration.user.register"
prefix_lst = "participant_registration.user.register.listener"
prefix_prt = "participant_registration.user.register.participant"
shared = "participant_registration.shared"

async def pr_cb_user_register(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, prefix_base, "listener.button"), callback_data="pr_cb_reg_lst_frm_section")
  keyboard.button(text=getstr(lang, prefix, "participant.button"), callback_data="pr_cb_reg_prt_frm_section")
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  keyboard.adjust(2, 1, 1)

  await callback_query.message.edit_text(getstr(lang, prefix, "caption"), reply_markup=keyboard.as_markup())

# Listener ---------------------------------------------------------------------

async def pr_cb_reg_lst_frm_section(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_lst_frm_theme(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_lst_frm_faculty(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_lst_frm_course(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_lst_frm_on_success(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_lst_frm_on_failure(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

# Participant ------------------------------------------------------------------
async def pr_cb_reg_prt_frm_course(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_prt_frm_advisor(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_prt_frm_english_level(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_prt_frm_translator(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_prt_frm_on_success(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_prt_frm_on_failure(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

# Group member -----------------------------------------------------------------
async def pr_cb_reg_gm_frm_section(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_gm_frm_theme(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_gm_frm_amount(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

async def pr_cb_reg_gm_frm_on_success(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())

async def pr_cb_reg_gm_frm_on_failure(callback_query: types.CallbackQuery, bot: Bot) -> None:
  keyboard = InlineKeyboardBuilder()
  keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

  await callback_query.message.edit_text(getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup())