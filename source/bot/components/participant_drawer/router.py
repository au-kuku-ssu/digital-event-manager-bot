from aiogram import Bot, Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.participant_drawer.frontend import frontend_cb_pd_main

router = Router()

@router.callback_query(lambda c: c.data == "cb_pd_main")
async def cb_pd_main_menu(callback_query: types.CallbackQuery, bot: Bot) -> None:
  await frontend_cb_pd_main(callback_query, bot)