from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from os.path import join, dirname

from aiogram.types import CallbackQuery

from components.reports_evaluation.data.placeholder_jury import PLACEHOLDER_JURY
from components.reports_evaluation.data.placeholder_presentations import (
    PLACEHOLDER_PRESENTS,
)
from components.reports_evaluation.fsm_states import REAuthStates
from components.reports_evaluation.keyboards import (
    re_get_main_menu_keyboard,
    re_get_presentations_keyboard,
    re_get_back_keyboard,
)
from components.reports_evaluation.utils import re_check_access_code, re_ensure_auth
from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")


async def frontend_cb_re_auth(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Shows user prompt for entering access code.
    """
    await state.clear()
    lang = "ru"

    await state.set_state(REAuthStates.waiting_for_code)
    await callback_query.message.edit_text(
        getstr(lang, "reports_evaluation.auth.caption")
    )


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

    juror = await re_check_access_code(code)

    if juror:
        await state.update_data(jury_code=code)
        await state.set_state(REAuthStates.authorized)
        await frontend_re_show_main_menu(message, bot, state)
    else:
        await message.answer(getstr(lang, "reports_evaluation.auth.invalid_code"))

        # Code below spams a lot of windows, so the "back" button is turned off.
        # keyboard = re_get_back_keyboard(lang)
        # await message.answer(getstr(lang, "reports_evaluation.auth.invalid_code"), reply_markup=keyboard)


async def frontend_re_show_main_menu(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    """
    Handles showing main menu of reports evaluation.
    """
    lang = "ru"
    state_data = await state.get_data()
    jury_code = state_data.get("jury_code")
    jury_name = PLACEHOLDER_JURY[jury_code]["name"]

    keyboard = re_get_main_menu_keyboard(lang)
    await message.answer(
        getstr(lang, "reports_evaluation.menu.caption").format(jury_name=jury_name),
        reply_markup=keyboard,
    )


async def frontend_cb_re_show_presentations(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles showing presentation keyboard.
    """
    lang = "ru"
    page = int(callback_query.data.split(":")[1])

    # Check auth
    if not await re_ensure_auth(callback_query, bot, state):
        return

    # Fetch the presentations and generate the keyboard with the appropriate page
    caption, keyboard = re_get_presentations_keyboard(lang, PLACEHOLDER_PRESENTS, page)

    # Update the message with the new caption and keyboard
    await callback_query.message.edit_text(
        text=caption, reply_markup=keyboard, parse_mode="HTML"
    )


async def frontend_cb_re_choose_presentation(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles starting of report evaluation.
    """
    lang = "ru"

    # Check auth
    if not await re_ensure_auth(callback_query, bot, state):
        return

    pres_id = callback_query.data.split(":")[1]
    keyboard = re_get_back_keyboard(lang)

    await callback_query.message.edit_text(
        text=f"{getstr(lang, 'reports_evaluation.evaluation.caption')}\nPresentation ID: {pres_id}",
        reply_markup=keyboard,
    )
