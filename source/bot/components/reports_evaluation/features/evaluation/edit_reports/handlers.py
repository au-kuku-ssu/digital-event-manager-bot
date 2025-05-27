from aiogram import Bot
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from components.reports_evaluation.data.placeholder_presentations import (
    PLACEHOLDER_PRESENTS,
)
from components.reports_evaluation.features.evaluation.edit_reports.keyboards import (
    re_get_edit_results_keyboard,
    re_get_select_jury_keyboard,
)
from components.reports_evaluation.features.evaluation.keyboards import (
    re_get_presentations_keyboard,
    re_get_error_keyboard,
)
from components.reports_evaluation.utils import getstr, re_require_auth
from components.shared.db import Database


@re_require_auth
async def frontend_cb_re_edit_results(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles the callback query to display the results editing interface.

    This function checks if the user is a chairman (based on their auth code),
    fetches the appropriate results editing keyboard and caption, and updates
    the message to display the results table with the corresponding interactive buttons.
    """
    lang = "ru"

    # Get state data
    state_data = await state.get_data()
    auth_code = state_data["auth_code"]

    # Check if chair
    is_chairman = await db.get_jury_role_by_access_key(auth_code)

    if not is_chairman:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "not chairman")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    caption, keyboard = await re_get_edit_results_keyboard(lang, db)

    await callback_query.message.edit_text(text=caption, reply_markup=keyboard)


@re_require_auth
async def frontend_cb_re_edit_select_jury(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles jury selection during result editing by the chairman.

    Extracts the jury_code from the callback data, validates it against PLACEHOLDER_JURY,
    and if valid, stores it in FSMContext. Then generates a confirmation interface to proceed
    with editing the selected jury’s evaluation results. If the jury_code is invalid, shows an error.
    """
    lang = "ru"

    # TODO: Check hashed jury code with jury code in db

    jury_code = callback_query.data.split(":")[1]
    wrong_code = False

    juries = await db.get_all_juries_with_names()
    if jury_code not in [jury[0] for jury in juries]:
        wrong_code = True
    else:
        await state.update_data(editing_target_access_key=jury_code)

    caption, keyboard = re_get_select_jury_keyboard(lang, wrong_code)

    await callback_query.message.edit_text(text=caption, reply_markup=keyboard)


@re_require_auth
async def frontend_cb_re_edit_show_presentations(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Displays the list of presentations for result editing by the chairman.

    Fetches the currently selected jury_code from FSMContext and uses it to generate
    a paginated list of all presentations (regardless of review status). Intended for
    editing previously submitted evaluations. If no presentations are available,
    displays a fallback message.
    """
    # TODO: Currently almost a copy of frontend_cb_re_show_presentations
    lang = "ru"
    page = int(callback_query.data.split(":")[1])

    data = await state.get_data()
    jury_code = data["jury_code"]

    # print(f"[DEBUG] {data}")

    # Fetch the presentations and generate the keyboard with the appropriate page
    caption, keyboard = re_get_presentations_keyboard(
        lang, PLACEHOLDER_PRESENTS, jury_code, page, edit=True
    )

    # If no presents available
    if not caption:
        await callback_query.message.edit_text(
            text=getstr(lang, "reports_evaluation.presents.no_presents_available"),
            reply_markup=keyboard,
        )
        return

    # Update the message with the new caption and keyboard
    await callback_query.message.edit_text(
        text=caption, reply_markup=keyboard, parse_mode="HTML"
    )
