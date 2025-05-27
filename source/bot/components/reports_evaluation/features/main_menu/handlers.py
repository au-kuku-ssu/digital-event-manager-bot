from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from components.reports_evaluation.features.main_menu.keyboards import (
    re_get_main_menu_keyboard,
    re_get_return_to_main_menu_keyboard,
)
from components.reports_evaluation.utils import (
    re_require_auth,
    re_delete_auth_messages,
    getstr,
)
from components.shared.db import Database


@re_require_auth
async def frontend_cb_re_main_menu(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles showing main menu of reports evaluation.
    """
    lang = "ru"
    state_data = await state.get_data()

    # Delete auth messages
    if "re_auth_message_ids" in state_data:
        await re_delete_auth_messages(state, callback_query.message.chat.id, bot)

    auth_code = state_data.get("auth_code")

    # Update jury_code to auth_code
    await state.update_data(
        jury_code=auth_code, pres_id=None, scores=None, pres_comments=None
    )

    jury_name = await db.get_jury_name_by_access_key(auth_code)

    keyboard = re_get_main_menu_keyboard(lang)
    await callback_query.message.edit_text(
        getstr(lang, "reports_evaluation.menu.caption").format(jury_name=jury_name),
        reply_markup=keyboard,
    )


async def frontend_cb_re_return_to_main_menu(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles returning to main menu. Exists because state data must be reset.
    """
    lang = "ru"
    await state.clear()

    caption, keyboard = re_get_return_to_main_menu_keyboard(lang)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )
