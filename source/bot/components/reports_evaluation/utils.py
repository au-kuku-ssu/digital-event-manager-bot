from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from components.main_menu.frontend import frontend_cb_mm_main
from components.reports_evaluation.data.placeholder_jury import PLACEHOLDER_JURY


async def re_check_access_code(code: str):
    """
    Checks if access code is valid.
    """
    jury_data = PLACEHOLDER_JURY

    for juror in jury_data:
        if juror == code:
            return juror

    return None


async def re_ensure_auth(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Ensures that the user is authenticated. If not, returns the user to the main menu (cb_mm_main).
    """
    state_data = await state.get_data()

    if "jury_code" not in state_data:
        await callback_query.answer(
            text="Auth failed",
            reply_markup=types.ReplyKeyboardRemove(),
            show_alert=True,
        )
        await frontend_cb_mm_main(callback_query, bot)
        return False
    return True
