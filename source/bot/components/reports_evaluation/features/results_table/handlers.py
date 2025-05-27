from aiogram import Bot
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from components.reports_evaluation.data.placeholder_presentations import (
    PLACEHOLDER_PRESENTS,
)
from components.reports_evaluation.features.results_table.keyboards import (
    re_get_results_table_keyboard,
)
from components.reports_evaluation.utils import re_require_auth
from components.shared.db import Database


@re_require_auth
async def frontend_cb_re_results_table(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles showing results table to user.
    """
    lang = "ru"

    page = int(callback_query.data.split(":")[1])

    # Fetch comprehensive presentation data including scores and juror details
    presentations_from_db = await db.get_presentations_with_scores_and_details()

    caption, keyboard = re_get_results_table_keyboard(
        lang, presentations_from_db, page=page
    )

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )
