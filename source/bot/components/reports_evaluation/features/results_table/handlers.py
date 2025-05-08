from aiogram import Bot
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from components.reports_evaluation.data.placeholder_jury import PLACEHOLDER_JURY
from components.reports_evaluation.data.placeholder_presentations import (
    PLACEHOLDER_PRESENTS,
)
from components.reports_evaluation.features.results_table.keyboards import (
    re_get_results_table_keyboard,
)
from components.reports_evaluation.utils import re_require_auth


@re_require_auth
async def frontend_cb_re_results_table(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles showing results table to user.
    """
    lang = "ru"

    page = int(callback_query.data.split(":")[1])

    caption, keyboard = re_get_results_table_keyboard(
        lang, PLACEHOLDER_PRESENTS, PLACEHOLDER_JURY, page
    )

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )
