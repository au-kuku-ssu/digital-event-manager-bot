from aiogram import Bot, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from components.main_menu.frontend import (
    frontend_cmd_mm_start,
    frontend_cb_mm_main,
    frontend_cb_mm_settings,
)

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, bot: Bot) -> None:
    await frontend_cmd_mm_start(message, bot)


@router.callback_query(lambda c: c.data == "cb_locale_ru")
async def callback_russian_language(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(lang="ru")
    await frontend_cb_mm_main(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "cb_locale_en")
async def callback_english_language(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(lang="en")
    await frontend_cb_mm_main(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "cb_mm_main")
async def callback_main_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_mm_main(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "cb_mm_settings")
async def callback_main_menu_settings(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_mm_settings(callback_query, bot, state)
