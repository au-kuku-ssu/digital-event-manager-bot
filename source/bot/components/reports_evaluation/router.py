from aiogram import Bot, Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.reports_evaluation.frontend import frontend_cb_re_main

router = Router()

@router.callback_query(lambda c: c.data == "cb_re_main")
async def cb_re_main_menu(callback_query: types.CallbackQuery, bot: Bot) -> None:
  await frontend_cb_re_main(callback_query, bot)