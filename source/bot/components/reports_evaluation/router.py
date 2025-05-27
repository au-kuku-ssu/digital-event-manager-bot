from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from components.reports_evaluation.features.auth.handlers import (
    frontend_cb_re_auth,
    frontend_st_re_process_code,
)
from components.reports_evaluation.features.evaluation.edit_reports.handlers import (
    frontend_cb_re_edit_results,
    frontend_cb_re_edit_show_presentations,
    frontend_cb_re_edit_select_jury,
)
from components.reports_evaluation.features.evaluation.handlers import (
    frontend_cb_re_show_presentations,
    frontend_cb_re_eval_choose_presentation,
    frontend_cb_re_eval_handle_score,
    frontend_cb_re_eval_return_to_score,
    frontend_cb_re_eval_comment,
    frontend_st_re_eval_comment,
    frontend_cb_re_eval_marks_accepted,
    frontend_cb_re_eval_back_to_summary,
)
from components.reports_evaluation.features.main_menu.handlers import (
    frontend_cb_re_main_menu,
    frontend_cb_re_return_to_main_menu,
)
from components.reports_evaluation.features.results_table.handlers import (
    frontend_cb_re_results_table,
)
from components.reports_evaluation.fsm_states import REAuthStates, REEvaluationStates
from components.shared.db import Database

router = Router()


# Authorization
@router.callback_query(lambda c: c.data == "cb_re_main")
async def cb_re_main_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Triggers the authentication process.
    """
    await frontend_cb_re_auth(callback_query, bot, state)


@router.message(REAuthStates.waiting_for_code)
async def st_re_process_code(
    message: types.Message, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Processes code entered by user.
    """
    await frontend_st_re_process_code(message, bot, state, db)


# Main menu
@router.callback_query(lambda c: c.data == "cb_re_main_menu")
async def cb_re_show_main_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers reports evaluation main menu. May trigger after successful authentication or be called in features.
    """
    await frontend_cb_re_main_menu(callback_query, bot, state, db)


@router.callback_query(lambda c: c.data == "cb_re_return_to_main_menu")
async def cb_re_return_to_mm_main_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_re_return_to_main_menu(callback_query, bot, state)


# Presents
@router.callback_query(F.data.startswith("cb_re_pres_page:"))
async def cb_re_change_pres_page(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers showing presentations information to the user.
    """
    await frontend_cb_re_show_presentations(callback_query, bot, state, db)


# Evaluation
@router.callback_query(F.data.startswith("cb_re_choose_pres:"))
async def cb_re_choose_presentation(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers report evaluation.
    """
    await frontend_cb_re_eval_choose_presentation(callback_query, bot, state, db)


@router.callback_query(F.data.startswith("cb_re_score:"))
async def cb_re_handle_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers evaluation criterion saving and showing the next criterion in reports evaluation.
    """
    await frontend_cb_re_eval_handle_score(callback_query, bot, state, db)


@router.callback_query(F.data.startswith("cb_re_return_to_score:"))
async def cb_re_return_to_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers returning to the previous criterion in reports evaluation.
    """
    await frontend_cb_re_eval_return_to_score(callback_query, bot, state, db)


@router.callback_query(lambda c: c.data == "cb_re_eval_comment")
async def cb_re_eval_comment(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers evaluation comment.
    """
    await frontend_cb_re_eval_comment(callback_query, bot, state, db)


@router.callback_query(lambda c: c.data == "cb_re_eval_marks_accepted")
async def cb_re_eval_marks_accepted(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers showing marks accepted or declined in reports evaluation.
    """
    await frontend_cb_re_eval_marks_accepted(callback_query, bot, state, db)


@router.message(REEvaluationStates.waiting_for_comment)
async def st_re_eval_comment(
    message: types.Message, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers menu showing 'continue' or 'edit' button after the comment.
    """
    await frontend_st_re_eval_comment(message, bot, state, db)


@router.callback_query(lambda c: c.data == "cb_re_eval_back_to_summary")
async def cb_re_eval_back_to_summary(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    await frontend_cb_re_eval_back_to_summary(callback_query, bot, state, db)


# Results table
@router.callback_query(F.data.startswith("cb_re_results_page:"))
async def cb_re_results_table(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers showing results table in reports evaluation.
    """
    await frontend_cb_re_results_table(callback_query, bot, state, db)


# Edit results
@router.callback_query(lambda c: c.data == "cb_re_edit_results")
async def cb_re_edit_results(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers showing jury selection menu.
    """
    await frontend_cb_re_edit_results(callback_query, bot, state, db)


@router.callback_query(F.data.startswith("cb_re_edit_select_jury:"))
async def cb_re_edit_select_jury(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers showing continue button after selecting jury member to edit.
    """
    await frontend_cb_re_edit_select_jury(callback_query, bot, state, db)


@router.callback_query(F.data.startswith("cb_re_edit_pres_page:"))
async def cb_re_edit_change_pres_page(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Triggers showing presentation choose menu to edit.
    """
    await frontend_cb_re_edit_show_presentations(callback_query, bot, state, db)
