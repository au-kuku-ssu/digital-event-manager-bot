from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from components.reports_evaluation.frontend import (
    frontend_cb_re_auth,
    frontend_st_re_process_code,
    frontend_cb_re_show_presentations,
    frontend_cb_re_choose_presentation,
    frontend_cb_re_handle_eval_score,
    frontend_cb_re_return_to_score,
    frontend_cb_re_eval_comment,
    frontend_cb_re_skip_comments,
    frontend_st_re_eval_comment,
)
from components.reports_evaluation.fsm_states import REAuthStates, REEvaluationStates

router = Router()


# Authorization
@router.callback_query(lambda c: c.data == "cb_re_main")
async def cb_re_main_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_re_auth(callback_query, bot, state)


@router.message(REAuthStates.waiting_for_code)
async def st_re_process_code(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await frontend_st_re_process_code(message, bot, state)


# Presents
@router.callback_query(F.data.startswith("cb_re_pres_page:"))
async def cb_re_change_pres_page(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_re_show_presentations(callback_query, bot, state)


# Evaluation
@router.callback_query(F.data.startswith("cb_re_choose_pres:"))
async def cb_re_choose_presentation(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_re_choose_presentation(callback_query, bot, state)


@router.callback_query(F.data.startswith("cb_re_score:"))
async def cb_re_handle_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_re_handle_eval_score(callback_query, bot, state)


@router.callback_query(F.data.startswith("cb_re_return_to_score:"))
async def cb_re_return_to_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_re_return_to_score(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "cb_re_eval_comment")
async def cb_re_eval_comment(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_re_eval_comment(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "cb_re_skip_comment")
async def cb_re_skip_comment(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await frontend_cb_re_skip_comments(callback_query, bot, state)


@router.message(REEvaluationStates.waiting_for_comment)
async def st_re_eval_comment(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await frontend_st_re_eval_comment(message, bot, state)
