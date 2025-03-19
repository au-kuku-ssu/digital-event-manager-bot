from aiogram import Bot, Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.program_generator.frontend import frontend_cb_pg_main

router = Router()

@router.callback_query(lambda c: c.data == "cb_pg_main")
async def cb_pg_main_menu(callback_query: types.CallbackQuery, bot: Bot) -> None:
  await frontend_cb_pg_main(callback_query, bot)