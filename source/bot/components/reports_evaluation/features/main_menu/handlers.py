from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from components.reports_evaluation.data.placeholder_jury import PLACEHOLDER_JURY
from components.reports_evaluation.features.main_menu.keyboards import (
    re_get_main_menu_keyboard,
)
from components.reports_evaluation.utils import (
    re_require_auth,
    re_delete_auth_messages,
    getstr,
)


@re_require_auth
async def frontend_cb_re_main_menu(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles showing main menu of reports evaluation.
    """
    lang = "ru"
    state_data = await state.get_data()

    # Delete auth messages
    if "re_auth_message_ids" in state_data:
        print("here")
        await re_delete_auth_messages(state, callback_query.message.chat.id, bot)

    jury_code = state_data.get("jury_code")
    jury_name = PLACEHOLDER_JURY[jury_code]["name"]

    keyboard = re_get_main_menu_keyboard(lang)
    await callback_query.message.edit_text(
        getstr(lang, "reports_evaluation.menu.caption").format(jury_name=jury_name),
        reply_markup=keyboard,
    )
