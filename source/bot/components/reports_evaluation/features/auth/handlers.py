from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
import logging

from components.reports_evaluation.features.auth.keyboards import (
    re_get_auth_continue_keyboard,
    re_get_auth_main_menu_keyboard,
)
from components.reports_evaluation.fsm_states import REAuthStates
from components.reports_evaluation.utils import (
    re_add_auth_message,
    re_check_access_code,
    getstr,
    re_delete_auth_messages,
)
from components.shared.db import Database


async def frontend_cb_re_auth(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Shows user prompt for entering access code.
    """
    await state.clear()
    lang = "ru"

    await state.set_state(REAuthStates.waiting_for_code)

    # print(f"[DEBUG] {getstr(lang, 'reports_evaluation.auth.caption')}")

    msg = await callback_query.message.edit_text(
        getstr(lang, "reports_evaluation.auth.caption")
    )

    await re_add_auth_message(state, msg.message_id)


async def frontend_st_re_process_code(
    message: types.Message, bot: Bot, state: FSMContext, db: Database
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

    # Pass the db instance to re_check_access_code
    is_chairman = await re_check_access_code(db, code)
    logging.info(f"is_chairman: {is_chairman}")

    if is_chairman is not None:
        await state.set_state(REAuthStates.authorized)
        # Store both auth_code and the is_chairman status
        await state.update_data(
            auth_code=code, auth_attempts=0, is_chairman=is_chairman
        )

        caption, keyboard = re_get_auth_continue_keyboard(lang)

        await message.answer(
            text=caption,
            reply_markup=keyboard,
        )
    else:
        # Increase auth_attempts count
        data = await state.get_data()
        attempts = data.get("auth_attempts", 0) + 1
        await state.update_data(auth_attempts=attempts)

        # Save invalid code message for deletion
        msg = await message.answer(getstr(lang, "reports_evaluation.auth.invalid_code"))
        await re_add_auth_message(state, msg.message_id)

        # Check if the number of attempts more than 3
        if attempts >= 3:
            await re_delete_auth_messages(state, message.chat.id, bot)
            await state.clear()
            caption, keyboard = re_get_auth_main_menu_keyboard(lang)
            await message.answer(
                text=caption,
                reply_markup=keyboard,
            )
