from aiogram import Bot, Router, types

from components.participant_registration.frontend import frontend_cb_pr_main

router = Router()


@router.callback_query(lambda c: c.data == "cb_pr_main")
async def cb_pr_main_menu(callback_query: types.CallbackQuery, bot: Bot) -> None:
    await frontend_cb_pr_main(callback_query, bot)
