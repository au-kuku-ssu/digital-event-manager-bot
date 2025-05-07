from aiogram import Bot, types
from aiogram.fsm.context import FSMContext


from components.reports_evaluation.features.auth.keyboards import (
    re_get_auth_continue_keyboard,
)
from components.reports_evaluation.fsm_states import REAuthStates
from components.reports_evaluation.utils import (
    re_add_auth_message,
    re_check_access_code,
    getstr,
)


async def frontend_cb_re_auth(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Shows user prompt for entering access code.
    """
    # TODO: Add reply button to return to main_menu
    await state.clear()
    lang = "ru"

    await state.set_state(REAuthStates.waiting_for_code)

    print(f"[DEBUG] {getstr(lang, 'reports_evaluation.auth.caption')}")

    msg = await callback_query.message.edit_text(
        getstr(lang, "reports_evaluation.auth.caption")
    )

    await re_add_auth_message(state, msg.message_id)


async def frontend_st_re_process_code(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    """
    Handles juror authorization based on input code.
    - On success: stores code, sets state, shows main menu.
    - On failure: shows error message with a back button.
    """
    lang = "ru"
    code = message.text.strip()

    # Save user message
    await re_add_auth_message(state, message.message_id)

    juror = await re_check_access_code(code)

    if juror:
        await state.update_data(jury_code=code)
        await state.set_state(REAuthStates.authorized)

        caption, keyboard = re_get_auth_continue_keyboard(lang)

        await message.answer(
            text=caption,
            reply_markup=keyboard,
        )
    else:
        # Save invalid code message for deletion
        msg = await message.answer(getstr(lang, "reports_evaluation.auth.invalid_code"))
        await re_add_auth_message(state, msg.message_id)
